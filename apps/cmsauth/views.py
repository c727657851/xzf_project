from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import LoginForm,RegisterForm
from utils import restful
from .models import User
from utils.captcha import Captcha  # 导入验证码类库
from io import BytesIO  # 管道  保存流数据
from django.core.cache import cache
from utils.aliyun_sms import send_sms

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

# 注册 的视图函数  
def register_view(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = User.objects.create_user(telephone=telephone,username=username,password=password)
        return restful.success()
    else:
        return restful.params_error(message=form.get_errors())
def logout_view(request):
    logout(request)
    return redirect(reverse('index'))


# 图形验证码
def image_captcha(request):
    text,image = Captcha.gene_graph_captcha()
    # 图片是一个流数据 也就是存到一个管道中 不像字符串可以用容器保存
    out = BytesIO()  # 创建一个管道
    image.save(out,'png')  # 图片保存
    # 读取时候从0开始读 为了防止读不到数据 指针回0
    out.seek(0)  # 指针回0
    # 把图片返回到浏览器上  通过response对象返回到浏览器上
    response = HttpResponse(content_type='image/png')
    response.write(out.read())
    response['Content-length'] = out.tell()
    cache.set(text.lower(), text.lower(), 5*60)  # 缓存中一份   用于做对比
    return response

def sms_captcha(request):
    code = Captcha.gene_num(number=6)  # 生成随机数字 六位
    print(code)

    # 接收手机号
    #/sms_captcha/?telephone=
    telephone = request.GET.get('telephone')
    cache.set(telephone,code,5*60)  # 两分钟有效
    print('cache中的验证码',cache.get(telephone))
    # send_sms(telephone,code)
    # 调用第三方发送短信验证码接口
    return restful.success()
