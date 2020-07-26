from django.shortcuts import render
from apps.news.models import NewsCategory,News
from django.conf import settings
from django.http import Http404
from .serializers import NewsSerializers
from utils import restful
# Create your views here.
def index(request):
    count = settings.ONE_PAGE_NEWS_COUNT
    newses = News.objects.select_related('category','author').all()[0:count]
    categories = NewsCategory.objects.all()
    context = {
        'newses': newses,
        'categories': categories,
    }
    return render(request,'news/index.html',context=context)

def news_detail(request,news_id):
    try:
        news = News.objects.select_related('category','author').get(pk=news_id)
        context = {
            'news': news
        }
        return render(request,'news/news_detail.html',context=context)
    except News.DoesNotExist:
        raise Http404

def news_list(request):
    newses = News.objects.select_related('category','author').all()
    serializer = NewsSerializers(newses,many=True)  # 每一条都要序列化成json
    data = serializer.data
    return restful.result(data=data)