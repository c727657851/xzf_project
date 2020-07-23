from django import forms
from django.core import validators
from apps.forms import FormMixin

class LoginForm(forms.Form,FormMixin):
    telephone = forms.CharField(max_length=11,validators=[validators.RegexValidator(r'1[3-9]\d{9}',message='请输入正确的手机号')])
    password = forms.CharField(max_length=20,min_length=6,error_messages={'max_length':'密码最长不能超过20位','min_length':'密码不能少于6位'})
    remember = forms.IntegerField(required=False)
