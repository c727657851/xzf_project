from django.shortcuts import render
# Create your views here.
def index(request):
    return render(request,'cms/login.html')

def register(request):
    return render(request,'cms/register.html')
