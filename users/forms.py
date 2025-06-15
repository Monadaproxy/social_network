from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Profile


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин:ㅤㅤ', widget=forms.TextInput(attrs={'class' : 'form-input'}))
    password = forms.CharField(label='Пароль:ㅤㅤ', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(label='Электронная почта:ㅤㅤ', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    username = forms.CharField(label='Придумайте логин:ㅤㅤ', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Придумайте пароль:ㅤㅤ', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повторите пароль:ㅤㅤ', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'})
        }

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 3,
                'maxlength': 60,
                'placeholder': 'Ваш статус (макс. 60 символов)'
            }),
        }


class AvatarUploadForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['avatar']
        widgets = {
            'avatar' : forms.FileInput(attrs={
                'style' : 'display: none; width: 50px; height: 50px',
                'id' : 'avatar-upload',
                'accept' : 'image/*'
            })
        }




