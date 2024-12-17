from django.contrib import admin
from django.utils.html import format_html
from .models import UserInfo, FeedInfo, UserAccess, CommentInfo, FeedDesc, CommentDesc, MediaFile
from django.urls import path
from django.shortcuts import render
from django.conf import settings
import os

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
    list_display = ('media_id', 'file_name', 'extension_type', 'feed', 'media_number', 'preview')
    list_filter = ('extension_type',)
    search_fields = ('file_name',)
    ordering = ('-media_id',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('media-browser/', self.admin_site.admin_view(self.media_browser_view), name='media-browser'),
        ]
        return custom_urls + urls

    def media_browser_view(self, request):
        media_dir = settings.MEDIA_ROOT
        files = []
        
        for root, dirs, filenames in os.walk(media_dir):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                rel_path = os.path.relpath(file_path, media_dir)
                file_size = os.path.getsize(file_path)
                file_type = os.path.splitext(filename)[1][1:].upper()
                
                files.append({
                    'name': filename,
                    'path': rel_path,
                    'size': self.format_file_size(file_size),
                    'type': file_type,
                    'url': os.path.join(settings.MEDIA_URL, rel_path)
                })

        context = {
            'title': 'Media Browser',
            'files': files,
            'media_url': settings.MEDIA_URL,
            'opts': self.model._meta,  # Django admin template에 필요한 옵션
        }
        
        return render(request, 'admin/media_browser.html', context)

    def format_file_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"

    def preview(self, obj):
        if obj.extension_type.lower() in ['jpg', 'jpeg', 'png', 'gif']:
            return format_html('<img src="/media/{}" style="max-height: 50px;"/>', obj.file_name)
        return '-'
    preview.short_description = 'Preview'
