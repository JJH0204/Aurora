from django.contrib.auth.models import AbstractUser
from django.db import models

# 사용자 정의 모델을 여기에 생성합니다.

class User(AbstractUser):
    """
    Aurora SNS를 위한 사용자 정의 모델
    """
    # 프로필 이미지를 저장할 필드
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    # 사용자 소개를 위한 필드
    bio = models.TextField(max_length=500, blank=True)
    # 웹사이트 URL을 저장할 필드
    website = models.URLField(max_length=200, blank=True)
    
    # 사용자가 팔로우하는 다른 사용자들을 저장하는 필드
    following = models.ManyToManyField(
        'self',  # 자기 자신을 참조
        through='UserFollow',  # 중간 테이블을 통해 연결
        related_name='followers',  # 역참조 이름
        symmetrical=False  # 비대칭 관계
    )

class UserFollow(models.Model):
    """
    사용자의 팔로우 관계를 추적하는 모델
    """
    # 팔로우하는 사용자
    follower = models.ForeignKey(User, related_name='following_relationships', on_delete=models.CASCADE)
    # 팔로우되는 사용자
    following = models.ForeignKey(User, related_name='follower_relationships', on_delete=models.CASCADE)
    # 팔로우가 생성된 시간
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 팔로우 관계의 유일성을 보장
        unique_together = ('follower', 'following')

class UserInfo(models.Model):
    # 사용자 ID, 자동 증가
    user_id = models.AutoField(primary_key=True)
    # 관리자 여부
    is_admin = models.BooleanField(default=0)
    # 공식 계정 여부
    is_official = models.BooleanField(default=0)
    # 사용자 닉네임
    nickname = models.CharField(max_length=50, null=True)
    # 친구 목록
    bf_list = models.TextField(null=True)

    class Meta:
        # 데이터베이스 테이블 이름 설정
        db_table = 'USER_INFO'