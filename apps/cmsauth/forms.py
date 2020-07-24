from django import forms
from django.core import validators
from apps.forms import FormMixin
from .models import User
from django.core.cache import cache   # 缓存

class LoginForm(forms.Form,FormMixin):
    telephone = forms.CharField(max_length=11,validators=[validators.RegexValidator(r'1[3-9]\d{9}',message='请输入正确的手机号')])
    password = forms.CharField(max_length=20,min_length=6,error_messages={'max_length':'密码最长不能超过20位','min_length':'密码不能少于6位'})
    remember = forms.IntegerField(required=False)

class RegisterForm(forms.Form,FormMixin):
    telephone = forms.CharField(max_length=11,validators=[validators.RegexValidator(r'1[3-9]\d{9}',message='请输入正确的手机号')])
    username = forms.CharField(max_length=20,min_length=3)
    password1 = forms.CharField(max_length=20,min_length=6, error_messages={'max_length':'密码最长不能超过20位','min_length':'密码不能少于6位'})
    password2 = forms.CharField(max_length=20,min_length=6, error_messages={'max_length':'密码最长不能超过20位','min_length':'密码不能少于6位'})
    image_captcha = forms.CharField(max_length=5,min_length=5)  # 图形验证码
    sms_captcha = forms.CharField(max_length=6,min_length=6)   # 短信验证码

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        image_captcha = cleaned_data.get('image_captcha')  # 用户输入的验证码
        cache_image_captcha = cache.get(image_captcha.lower())   # cache中的图形中的数字 根据输入的数字作为键
        if not cache_image_captcha or image_captcha != cache_image_captcha.lower():
            raise forms.ValidationError('图形验证码输入有误!')

        if password1 != password2:
            raise forms.ValidationError('两次密码输入不一致')

        telephone = cleaned_data.get('telephone')

        if User.objects.filter(telephone=telephone).exists():
            raise forms.ValidationError('该手机号已经被注册')

        return cleaned_data

