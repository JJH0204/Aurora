USE aurora_db;

SET FOREIGN_KEY_CHECKS = 1;
 
# 테이블 생성
CREATE TABLE USER_INFO (
    `user_id` INT UNSIGNED PRIMARY KEY,
    `is_admin` BOOLEAN,
    `is_official` BOOLEAN,
    `username` VARCHAR(50),
    `bf_list` VARCHAR(255)
);

CREATE TABLE FEED_INFO (
    `feed_id` INT UNSIGNED PRIMARY KEY,
    `user_id` INT UNSIGNED,
    `like_count` INT UNSIGNED,
    `feed_type` ENUM('type1', 'type2', 'type3'),
    FOREIGN KEY (user_id) REFERENCES USER_INFO(`user_id`)
);

CREATE TABLE USER_ACCESS (
    `user_id` INT UNSIGNED PRIMARY KEY,
    `email` VARCHAR(50),
    `password` VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES USER_INFO(`user_id`)
);

CREATE TABLE COMMENT_INFO (
    `comment_id` INT UNSIGNED PRIMARY KEY,
    `user_id` INT UNSIGNED,
    `feed_id` INT UNSIGNED,
    FOREIGN KEY (user_id) REFERENCES USER_INFO(`user_id`),
    FOREIGN KEY (feed_id) REFERENCES FEED_INFO(`feed_id`)
);

CREATE TABLE FEED_DESC (
    `feed_id` INT UNSIGNED PRIMARY KEY,
    `desc` TEXT,
    FOREIGN KEY (feed_id) REFERENCES FEED_INFO(`feed_id`)
);

CREATE TABLE COMMENT_DESC (
    `comment_id` INT UNSIGNED PRIMARY KEY,
    `desc` TEXT,
    FOREIGN KEY (comment_id) REFERENCES COMMENT_INFO(`comment_id`)
);

CREATE TABLE MEDIA_FILE (
    `media_id` INT UNSIGNED PRIMARY KEY,
    `file_name` VARCHAR(255),
    `extension_type` VARCHAR(10),
    `feed_id` INT UNSIGNED,
    `media_number` INT,
    FOREIGN KEY (feed_id) REFERENCES FEED_INFO(`feed_id`)
);

FLUSH PRIVILEGES;