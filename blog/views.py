from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

def index(request):
    context = {}
    context['title'] = '我的网站'
    context['welcome'] = '您好，欢迎来到我的网站'
    return render(request, 'blog/index.html', context)

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {}
    context['title'] = title
    context['post'] = post
    return render(request, 'blog/detail.html', context)