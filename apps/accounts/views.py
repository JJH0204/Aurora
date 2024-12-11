from django.shortcuts import render
from django.views.generic import DetailView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import User, UserFollow
from .forms import UserProfileForm
from django.shortcuts import render
from .models import UserInfo

# 뷰 클래스/함수들을 여기에 작성합니다.

class ProfileView(LoginRequiredMixin, DetailView):
    # 로그인한 사용자의 프로필을 보여주는 뷰
    model = User  # 사용할 모델
    template_name = 'accounts/profile.html'  # 사용할 템플릿
    context_object_name = 'profile_user'  # 템플릿에서 사용할 객체 이름

    def get_object(self):
        # 현재 로그인한 사용자 객체를 반환
        return self.request.user

class ProfileEditView(LoginRequiredMixin, UpdateView):
    # 프로필 수정을 위한 뷰
    model = User  # 수정할 모델
    form_class = UserProfileForm  # 사용할 폼 클래스
    template_name = 'accounts/profile_edit.html'  # 수정 페이지 템플릿
    success_url = reverse_lazy('profile')  # 수정 완료 후 리다이렉트할 URL

    def get_object(self):
        # 현재 로그인한 사용자 객체를 반환
        return self.request.user

class UserDetailView(DetailView):
    # 특정 사용자의 상세 정보를 보여주는 뷰
    model = User  # 사용할 모델
    template_name = 'accounts/user_detail.html'  # 사용할 템플릿
    context_object_name = 'profile_user'  # 템플릿에서 사용할 객체 이름
    slug_field = 'username'  # URL에서 사용할 필드
    slug_url_kwarg = 'username'  # URL 패턴에서 사용할 매개변수 이름

    def get_context_data(self, **kwargs):
        # 템플릿에 전달할 컨텍스트 데이터 추가
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # 현재 사용자가 프로필 주인을 팔로우하고 있는지 확인
            context['is_following'] = UserFollow.objects.filter(
                follower=self.request.user,
                following=self.get_object()
            ).exists()
        return context

class UserFollowView(LoginRequiredMixin, View):
    # 팔로우/언팔로우 기능을 처리하는 뷰
    def post(self, request, username):
        # 팔로우할 사용자 찾기
        user_to_follow = get_object_or_404(User, username=username)
        if request.user == user_to_follow:
            # 자기 자신을 팔로우하려는 경우 에러 반환
            return JsonResponse({'error': '자신을 팔로우할 수 없습니다.'}, status=400)
        
        # 팔로우 관계 생성 또는 가져오기
        follow, created = UserFollow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )
        
        # created가 False면 이미 존재하는 관계이므로 삭제(언팔로우)
        if not created:
            follow.delete()
            is_following = False
        else:
            is_following = True
            
        # 결과 반환
        return JsonResponse({
            'is_following': is_following,
            'follower_count': user_to_follow.followers.count(),
            'following_count': user_to_follow.following.count()
        })

def get_user(request, user_id):
    # 특정 사용자 정보를 조회하는 함수
    user = UserInfo.objects.get(user_id=user_id)
    return render(request, 'user_detail.html', {'user': user})

def create_user(request):
    # 새로운 사용자를 생성하는 함수
    new_user = UserInfo.objects.create(
        nickname='새로운유저',
        is_admin=False,
        is_official=False
    )
    return render(request, 'user_created.html', {'user': new_user})