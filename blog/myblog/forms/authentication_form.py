from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from ..utils.utils import is_password_valid

class SignUpForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'id': "inputUsername",
                'type': 'username',
                'placeholder': 'Имя пользователя'
            }
        ),
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control",
                'id': "inputPassword",
                'type': 'password',
                'placeholder': 'Пароль'
            }
        ),
    )

    repeat_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control",
                'id': "ReInputPassword",
                'type': 'password',
                'placeholder': 'Повторите пароль'
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data['password']
        confirm_password = cleaned_data['repeat_password']

        if password != confirm_password:
            raise forms.ValidationError(
                'Пароли не совпадают!'
            )
        
        elif not(is_password_valid(password)):
            raise forms.ValidationError(
                'Пароль не валидный'
            )
        
    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        user.save()
        auth = authenticate(**self.cleaned_data)
        return auth

class SignInForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True, 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'inputUsername'
            }
        )
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control mt-2",
            'id': "inputPassword",
        })
    )