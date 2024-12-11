# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sns.db'  # 데이터베이스 URI 설정
db = SQLAlchemy(app)

# USER_INFO 모델
class UserInfo(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    is_admin = db.Column(db.Boolean)
    is_official = db.Column(db.Boolean)
    nickname = db.Column(db.String)
    bf_list = db.Column(db.String)

# FEED_INFO 모델
class FeedInfo(db.Model):
    feed_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 자동 증가 설정
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.user_id'))
    feed_type = db.Column(db.String)

# 게시물 추가 함수
@app.route('/add_feed', methods=['POST'])
def add_feed():
    user_id = request.json.get('user_id')
    feed_type = request.json.get('feed_type')  # 'image' 또는 'text' 등

    # 새로운 피드 추가
    new_feed = FeedInfo(user_id=user_id, feed_type=feed_type)
    db.session.add(new_feed)
    db.session.commit()

    return jsonify({'message': 'Feed added successfully', 'feed_id': new_feed.feed_id}), 201

if __name__ == '__main__':
    db.create_all()  # 데이터베이스 테이블 생성
    app.run(debug=True)