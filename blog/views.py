from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = {}
    context['title'] = '我的网站'
    context['welcome'] = '您好，欢迎来到我的网站'
    return render(request, 'blog/index.html', context)
