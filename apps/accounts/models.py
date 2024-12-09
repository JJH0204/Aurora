from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    """
    Custom user model for Aurora SNS
    """
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    website = models.URLField(max_length=200, blank=True)
    
    following = models.ManyToManyField(
        'self',
        through='UserFollow',
        related_name='followers',
        symmetrical=False
    )

class UserFollow(models.Model):
    """
    Model to track user follows
    """
    follower = models.ForeignKey(User, related_name='following_relationships', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='follower_relationships', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
