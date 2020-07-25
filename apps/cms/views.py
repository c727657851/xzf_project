from django.shortcuts import render
from django.views.generic import View
from apps.news.models import NewsCategory
from utils import restful
from apps.cms.forms import WriteNewsForm
# Create your views here.

def index(request):
    return render(request,'cms/index.html')


class WriteNews(View):
    def get(self,request):
        categories = NewsCategory.objects.all()
        context = {
            'categories': categories
        }
        return render(request,'cms/write_news.html',context=context)

    def post(self):
        form = WriteNewsForm()
        if form.is_valid():
            pass



def news_category(request):
    categories = NewsCategory.objects.all()
    context = {
        'categories': categories
    }
    return render(request,'cms/news_category.html',context=context)

def add_news_category(request):
    name = request.POST.get('name')
    exists = NewsCategory.objects.filter(name=name).exists()
    if exists:
        return restful.params_error(message='该分类以及存在')
    else:
        NewsCategory.objects.create(name=name)
    return render(request,'cms/news_category.html')