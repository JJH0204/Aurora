from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse
from django.db import connection
from functools import wraps
from . import views

# 공식 계정 확인 데코레이터
def official_account_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT is_official 
                    FROM USER_INFO 
                    WHERE user_id = %s
                """, [request.user.id])
                result = cursor.fetchone()
                
                if not result or not result[0]:
                    return redirect('/')  # 권한이 없으면 홈으로 리다이렉트
                
            return view_func(request, *args, **kwargs)
        except Exception as e:
            print(f"Error checking official status: {str(e)}")
            return redirect('/')
    return _wrapped_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('post/', login_required(TemplateView.as_view(template_name='post.html')), name='post'),
    path('profile/', login_required(TemplateView.as_view(template_name='profile.html')), name='profile'),
    path('profile/<int:user_id>/', login_required(TemplateView.as_view(template_name='profile.html')), name='user_profile'),
    path('profile/edit/', login_required(TemplateView.as_view(template_name='profileEdit.html')), name='profile_edit'),
    path('aurora/', login_required(official_account_required(TemplateView.as_view(template_name='aurora.html'))), name='aurora'),
    path('api/signup', views.signup, name='signup'),
    path('api/login', views.login, name='login'),
    path('api/logout', views.logout, name='logout'),
    path('api/post', views.create_post, name='create_post'),
    path('api/profile', views.get_profile, name='get_profile'),
    path('api/user-posts', views.get_user_posts, name='get_user_posts'),
    path('api/user-friends', views.get_user_friends, name='get_user_friends'),
    path('api/update-profile/', views.update_profile, name='update_profile'),  
    path('api/feed-posts', views.get_feed_posts, name='get_feed_posts'),
    path('check-auth/', views.check_auth, name='check-auth'),
    path('api/like-post', views.like_post, name='like_post'),
    path('api/direct-query', views.direct_query, name='direct_query'),
    path('api/search_posts', views.search_posts, name='search_posts'),
    path('api/media-files', views.get_media_files, name='get_media_files'),
    path('view-file/<str:filename>', views.view_file, name='view_file'),
]

# Debug 모드일 때만 미디어 파일 서빙
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.PROFILE_URL, document_root=settings.PROFILE_ROOT)
