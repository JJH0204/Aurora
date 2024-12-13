USE aurora_db;

# 데이터베이스 문자셋 설정
ALTER DATABASE aurora_db CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;
 
# 테이블 생성
CREATE TABLE USER_INFO (
    `user_id` INT UNSIGNED PRIMARY KEY,
    `is_admin` BOOLEAN,
    `is_official` BOOLEAN,
    `username` VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    `bf_list` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    # 프로필 이미지 DB 추가
    `profile_image` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE FEED_INFO (
    `feed_id` INT UNSIGNED PRIMARY KEY,
    `user_id` INT UNSIGNED,
    `like_count` INT UNSIGNED,
    `feed_type` ENUM('type1', 'type2', 'type3'),
    FOREIGN KEY (user_id) REFERENCES USER_INFO(`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE USER_ACCESS (
    `user_id` INT UNSIGNED PRIMARY KEY,
    `email` VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    `password` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    FOREIGN KEY (user_id) REFERENCES USER_INFO(`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE COMMENT_INFO (
    `comment_id` INT UNSIGNED PRIMARY KEY,
    `user_id` INT UNSIGNED,
    `feed_id` INT UNSIGNED,
    FOREIGN KEY (user_id) REFERENCES USER_INFO(`user_id`),
    FOREIGN KEY (feed_id) REFERENCES FEED_INFO(`feed_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE FEED_DESC (
    `feed_id` INT UNSIGNED PRIMARY KEY,
    `desc` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    FOREIGN KEY (feed_id) REFERENCES FEED_INFO(`feed_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE COMMENT_DESC (
    `comment_id` INT UNSIGNED PRIMARY KEY,
    `desc` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    FOREIGN KEY (comment_id) REFERENCES COMMENT_INFO(`comment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE MEDIA_FILE (
    `media_id` INT UNSIGNED PRIMARY KEY,
    `file_name` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    `extension_type` VARCHAR(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    `feed_id` INT UNSIGNED,
    `media_number` INT,
    FOREIGN KEY (feed_id) REFERENCES FEED_INFO(`feed_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE FEED_LIKE (
    `user_id` INT UNSIGNED,
    `feed_id` INT UNSIGNED,
    `like_date` DATETIME,
    PRIMARY KEY (user_id, feed_id),
    FOREIGN KEY (user_id) REFERENCES USER_INFO(`user_id`),
    FOREIGN KEY (feed_id) REFERENCES FEED_INFO(`feed_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

# 테스트 데이터 삽입
INSERT INTO auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
VALUES ('pbkdf2_sha256$600000$bLtHI1gBXnLxQr1ZrM8GXoZP$6YZUv7YHKDZqCb0Nis5IxGsKyQUCXZoZcEQlnlp7=', NULL, 0, 'test_admin', '', '', 'test@aurora.com', 0, 1, NOW());

INSERT INTO USER_INFO (`user_id`, `is_admin`, `is_official`, `username`, `bf_list`)
VALUES (1, true, true, 'test_admin', NULL);

INSERT INTO USER_ACCESS (`user_id`, `email`, `password`)
VALUES (1, 'test@aurora.com', 'test1234');

# 테스트 게시물 데이터 삽입
INSERT INTO FEED_INFO (`feed_id`, `user_id`, `like_count`, `feed_type`) 
VALUES 
    (1, 1, 0, 'type1'),
    (2, 1, 0, 'type2'),
    (3, 1, 0, 'type3');

# 게시물 설명 추가
INSERT INTO FEED_DESC (`feed_id`, `desc`)
VALUES
    (1, '첫 번째 테스트 게시물입니다. type1 유형의 게시물 테스트'),
    (2, '두 번째 테스트 게시물입니다. type2 유형의 게시물 테스트'),
    (3, '세 번째 테스트 게시물입니다. type3 유형의 게시물 테스트');

# 미디어 파일 정보 추가
INSERT INTO MEDIA_FILE (`media_id`, `file_name`, `extension_type`, `feed_id`, `media_number`)
VALUES
    (1, 'test_image_1.jpg', 'jpg', 1, 1),
    (2, 'test_image_2.png', 'png', 2, 1),
    (3, 'test_video_1.mp4', 'mp4', 3, 1),
    (4, 'test_image_3.jpg', 'jpg', 3, 2);

FLUSH PRIVILEGES;