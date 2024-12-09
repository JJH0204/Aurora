from flask import Flask, render_template, jsonify, request
from datetime import datetime

app = Flask(__name__)

# 기본 설정
app.config.update(
    JSON_AS_ASCII=False,
    JSON_SORT_KEYS=False
)

@app.route('/')
def home():
    """메인 페이지"""
    return render_template('index.html')

@app.route('/api/health')
def health_check():
    """서버 상태 확인"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/hello', methods=['GET'])
def hello():
    """기본 API 엔드포인트"""
    return jsonify({
        'message': 'Hello, World!',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/greet', methods=['POST'])
def greet():
    """사용자 이름을 받아 인사하는 API"""
    data = request.get_json()
    name = data.get('name', 'Guest')
    return jsonify({
        'message': f'Hello, {name}!',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
