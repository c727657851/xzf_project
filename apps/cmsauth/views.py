from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import LoginForm
from utils import restful

@require_POST
def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        user = authenticate(request, username=telephone,password=password)
        if user:
            if user.is_active:
                login(request,user)
                if remember:
                    request.session.set_expiry(None)  # 默认保存两周
                else:
                    request.session.set_expiry(0)
                return restful.success()
            else:
                return restful.unauth(message='您的账号未激活')
        else:
            return restful.params_error(message='手机号或者密码错误')
    else:
        errors = form.get_errors()
        return restful.params_error(message=errors)

# 注册
def register_view(request):
    pass


