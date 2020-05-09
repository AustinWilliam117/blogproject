from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Post

def index(request):
    post_list = Post.objects.all()
    context = {}
    context['post_list'] = post_list
    return render(request, 'blog/index.html', context)

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {}
    context['title'] = title
    context['post'] = post
    return render(request, 'blog/detail.html', context)