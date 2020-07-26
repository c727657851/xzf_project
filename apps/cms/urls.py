from django.urls import path
from . import views
app_name = 'cms'

urlpatterns = [
    path('',views.index,name='index'),
    path('write_news/',views.WriteNews.as_view(),name='write_news'),
    path('news_category/',views.news_category,name='news_category'),
    path('add_news_category/',views.add_news_category,name='add_news_category'),
    path('qntoken/',views.qntoken,name='qntoken'),
    path('my_login/',views.my_login,name='my_login'),
    path('news_list/',views.NewsList.as_view(),name='news_list'),
]