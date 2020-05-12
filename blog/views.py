import markdown,re
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

from .models import Post, Category, Tag

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

    # 筛选当前博客大于创建时间的博客最后一条
    context['next_post'] = Post.objects.filter(created_time__gt=post.created_time).last()
    # 筛选当前博客小于创建时间的博客第一条
    context['previous_post'] = Post.objects.filter(created_time__lt=post.created_time).first()
    return render(request, 'blog/detail.html', context)

# 归档
def archive(request, year, month):
    archive_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

# 分类
def category(request, pk):
    # 记得在开始部分导入 Category 类
    cate = get_object_or_404(Category, pk=pk)
    category_list = Post.objects.filter(category=cate).order_by('-created_time')
    context = {}
    context['post_category'] = cate
    return render(request, 'blog/index.html', context)

# 标签
def tag(request, pk):
    # 记得在开始部分导入 Tag 类
    t = get_object_or_404(Tag, pk=pk)
    tag_list = Post.objects.filter(tags=t).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
