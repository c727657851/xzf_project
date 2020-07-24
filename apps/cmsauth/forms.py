from django import forms
from django.core import validators
from apps.forms import FormMixin
from .models import User

class LoginForm(forms.Form,FormMixin):
    telephone = forms.CharField(max_length=11,validators=[validators.RegexValidator(r'1[3-9]\d{9}',message='请输入正确的手机号')])
    password = forms.CharField(max_length=20,min_length=6,error_messages={'max_length':'密码最长不能超过20位','min_length':'密码不能少于6位'})
    remember = forms.IntegerField(required=False)

class RegisterForm(forms.Form,FormMixin):
    telephone = forms.CharField(max_length=11,validators=[validators.RegexValidator(r'1[3-9]\d{9}',message='请输入正确的手机号')])
    username = forms.CharField(max_length=20,min_length=3)
    email = forms.EmailField()
    password1 = forms.CharField(max_length=20,min_length=6,error_messages={'max_length':'密码最长不能超过20位','min_length':'密码不能少于6位'})
    password2 = forms.CharField(max_length=20,min_length=6,error_messages={'max_length':'密码最长不能超过20位','min_length':'密码不能少于6位'})

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('两次密码输入不一致')

        telephone = cleaned_data.get('telephone')

        if User.objects.filter(telephone=telephone).exists():
            raise forms.ValidationError('该手机号已经被注册')
        email = cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮件已经注册')
        return cleaned_data

