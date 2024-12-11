from django.contrib import admin
from .models import UserInfo, FeedInfo, UserAccess, CommentInfo, FeedDesc, CommentDesc, MediaFile

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'is_admin', 'is_official')
    list_filter = ('is_admin', 'is_official')
    search_fields = ('username',)
    ordering = ('user_id',)

@admin.register(FeedInfo)
class FeedInfoAdmin(admin.ModelAdmin):
    list_display = ('feed_id', 'user', 'like_count', 'feed_type')
    list_filter = ('feed_type',)
    search_fields = ('user__username',)
    ordering = ('-feed_id',)

@admin.register(UserAccess)
class UserAccessAdmin(admin.ModelAdmin):
    list_display = ('user', 'email')
    search_fields = ('email', 'user__username')
    ordering = ('user',)

@admin.register(CommentInfo)
class CommentInfoAdmin(admin.ModelAdmin):
    list_display = ('comment_id', 'user', 'feed')
    search_fields = ('user__username',)
    list_filter = ('feed',)
    ordering = ('-comment_id',)

@admin.register(FeedDesc)
class FeedDescAdmin(admin.ModelAdmin):
    list_display = ('feed', 'desc')
    search_fields = ('desc',)
    ordering = ('feed',)

@admin.register(CommentDesc)
class CommentDescAdmin(admin.ModelAdmin):
    list_display = ('comment', 'desc')
    search_fields = ('desc',)
    ordering = ('comment',)

@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ('media_id', 'file_name', 'extension_type', 'feed', 'media_number')
    list_filter = ('extension_type',)
    search_fields = ('file_name',)
    ordering = ('-media_id',)
