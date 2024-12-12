from django.db import models

class UserInfo(models.Model):
    user_id = models.AutoField(primary_key=True)
    is_admin = models.BooleanField(default=False)
    is_official = models.BooleanField(default=False)
    username = models.CharField(max_length=50)
    bf_list = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'USER_INFO'

class FeedInfo(models.Model):
    feed_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    like_count = models.PositiveIntegerField(default=0)
    feed_type = models.CharField(max_length=10, choices=[
        ('type1', 'Type 1'),
        ('type2', 'Type 2'),
        ('type3', 'Type 3')
    ])

    class Meta:
        db_table = 'FEED_INFO'

class UserAccess(models.Model):
    user = models.OneToOneField(UserInfo, primary_key=True, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'USER_ACCESS'

class CommentInfo(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    feed = models.ForeignKey(FeedInfo, on_delete=models.CASCADE)

    class Meta:
        db_table = 'COMMENT_INFO'

class FeedDesc(models.Model):
    feed = models.OneToOneField(FeedInfo, primary_key=True, on_delete=models.CASCADE)
    desc = models.TextField()

    class Meta:
        db_table = 'FEED_DESC'

class CommentDesc(models.Model):
    comment = models.OneToOneField(CommentInfo, primary_key=True, on_delete=models.CASCADE)
    desc = models.TextField()

    class Meta:
        db_table = 'COMMENT_DESC'

class MediaFile(models.Model):
    media_id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=255)
    extension_type = models.CharField(max_length=10)
    feed = models.ForeignKey(FeedInfo, on_delete=models.CASCADE)
    media_number = models.IntegerField()

    class Meta:
        db_table = 'MEDIA_FILE'

class FeedLike(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    feed = models.ForeignKey(FeedInfo, on_delete=models.CASCADE)
    like_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'FEED_LIKE'
        unique_together = ('user', 'feed')
