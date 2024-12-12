from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('post/', login_required(TemplateView.as_view(template_name='post.html')), name='post'),
    path('profile/', login_required(TemplateView.as_view(template_name='profile.html')), name='profile'),
    path('profile/<int:user_id>/', login_required(TemplateView.as_view(template_name='profile.html')), name='user_profile'),
    path('profile/edit/', login_required(TemplateView.as_view(template_name='profileEdit.html')), name='profile_edit'),
    path('save/', login_required(TemplateView.as_view(template_name='save.html')), name='save'),
    path('api/signup', views.signup, name='signup'),
    path('api/login', views.login, name='login'),
    path('api/logout', views.logout, name='logout'),
    path('api/post', views.create_post, name='create_post'),
    path('api/profile', views.get_profile, name='get_profile'),
    path('api/update-profile', views.update_profile, name='update_profile'),
    path('api/user-posts', views.get_user_posts, name='get_user_posts'),
    path('api/user-friends', views.get_user_friends, name='get_user_friends'),
    path('api/liked-posts', views.get_liked_posts, name='get_liked_posts'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
