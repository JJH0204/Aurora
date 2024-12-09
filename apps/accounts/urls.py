from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProfileView.as_view(), name='profile'),
    path('edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('<str:username>/', views.UserDetailView.as_view(), name='user_detail'),
    path('<str:username>/follow/', views.UserFollowView.as_view(), name='user_follow'),
]
