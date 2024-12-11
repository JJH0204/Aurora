#!/bin/bash

# DB 스크립트 생성
cat > db_script.sql << 'EOF'
DROP DATABASE IF EXISTS aurora_db;
CREATE DATABASE aurora_db;
USE aurora_db;

# 기존 테이블들이 있다면 삭제
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS USER_INFO;
DROP TABLE IF EXISTS FEED_INFO;
DROP TABLE IF EXISTS USER_ACCESS;
DROP TABLE IF EXISTS COMMENT_INFO;
DROP TABLE IF EXISTS FEED_DESC;
DROP TABLE IF EXISTS COMMENT_DESC;
DROP TABLE IF EXISTS MEDIA_FILE;
SET FOREIGN_KEY_CHECKS = 1;
 
# 테이블 생성
CREATE TABLE USER_INFO (
    user_id INT UNSIGNED PRIMARY KEY,
    is_admin BOOLEAN,
    is_official BOOLEAN,
    nickname VARCHAR(50),
    bf_list VARCHAR(255)
);

CREATE TABLE FEED_INFO (
    feed_id INT UNSIGNED PRIMARY KEY,
    user_id INT UNSIGNED,
    like_count INT UNSIGNED,
    feed_type ENUM('type1', 'type2', 'type3'),
    FOREIGN KEY (user_id) REFERENCES USER_INFO(user_id)
);

CREATE TABLE USER_ACCESS (
    user_id INT UNSIGNED PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES USER_INFO(user_id)
);

CREATE TABLE COMMENT_INFO (
    comment_id INT UNSIGNED PRIMARY KEY,
    user_id INT UNSIGNED,
    feed_id INT UNSIGNED,
    FOREIGN KEY (user_id) REFERENCES USER_INFO(user_id),
    FOREIGN KEY (feed_id) REFERENCES FEED_INFO(feed_id)
);

CREATE TABLE FEED_DESC (
    feed_id INT UNSIGNED PRIMARY KEY,
    `desc` TEXT,
    FOREIGN KEY (feed_id) REFERENCES FEED_INFO(feed_id)
);

CREATE TABLE COMMENT_DESC (
    comment_id INT UNSIGNED PRIMARY KEY,
    `desc` TEXT,
    FOREIGN KEY (comment_id) REFERENCES COMMENT_INFO(comment_id)
);

CREATE TABLE MEDIA_FILE (
    media_id INT UNSIGNED PRIMARY KEY,
    file_name VARCHAR(255),
    extension_type VARCHAR(10),
    feed_id INT UNSIGNED,
    media_number INT,
    FOREIGN KEY (feed_id) REFERENCES FEED_INFO(feed_id)
);
EOF

# MySQL 컨테이너 이름 설정
CONTAINER_NAME="aurora-app"

# 스크립트 파일을 컨테이너에 복사
docker cp db_script.sql $CONTAINER_NAME:/db_script.sql

# 컨테이너 내부에서 MySQL 스크립트 실행
docker exec -i $CONTAINER_NAME mysql -u root -p'qwer' < db_script.sql

# 임시 파일 삭제
rm db_script.sql

echo "Database setup completed!" 