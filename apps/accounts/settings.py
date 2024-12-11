DATABASES = {
    'default': {  # 기본 데이터베이스 설정
        'ENGINE': 'django.db.backends.mysql',  # MySQL 데이터베이스 엔진 사용
        'NAME': 'aurora_db',  # 사용할 데이터베이스 이름
        'USER': 'root',  # 데이터베이스 접속 사용자
        'PASSWORD': 'rootpassword',  # 데이터베이스 접속 비밀번호
        'HOST': 'localhost',  # 데이터베이스 서버 주소 
        'PORT': '3306',  # MySQL 서버 포트
        'OPTIONS': {  # 추가 옵션 설정
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"  # SQL 모드를 엄격한 트랜잭션 테이블로 설정
        }
    }
}
