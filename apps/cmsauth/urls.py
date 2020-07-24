from django.urls import path
from . import views
app_name = 'cmsauth'

urlpatterns = [
    path('login/',views.login_view,name='login'),
    path('register/',views.register_view,name='register'),
    path('sms_captcha/',views.sms_captcha,name='sms_captcha'),
    path('image_captcha/',views.image_captcha,name='image_captcha'),
]