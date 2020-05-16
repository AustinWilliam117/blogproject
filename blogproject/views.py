from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from blog.models import Post, Category, Tag

def search(request):
    search_words = request.GET.get('wd', '').strip()

    # 分词：按空格 & | ~
    condition = None
    for word in search_words.split(' '):
        if condition is None:
            condition = Q(title__icontains=word)
        else:
            condition = condition | Q(title__icontains=word)

    search_posts = []
    if condition is not None:
        # 筛选：搜索
        search_posts = Post.objects.filter(condition)

    # 分页
    paginator = Paginator(search_posts, 10)
    page_num = request.GET.get('page', 1)
    page_of_posts = paginator.get_page(page_num)

    context = {}
    context['search_words'] = search_words
    context['search_posts_count'] = search_posts.count()
    context['page_of_posts'] = page_of_posts
    return render(request, 'search.html', context)