import markdown,re
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

from .models import Post

def index(request):
    post_list = Post.objects.all()
    context = {}
    context['post_list'] = post_list
    return render(request, 'blog/index.html', context)

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {}

    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        # 记得在顶部引入 TocExtension 和 slugify
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''

    context['post'] = post
    return render(request, 'blog/detail.html', context)