from django import forms
from .models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_image', 'bio', 'website']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': '자기소개를 입력하세요...'}),
            'website': forms.URLInput(attrs={'placeholder': 'https://'}),
        }
