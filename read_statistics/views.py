import datetime
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from read_statistics.utils import get_week_read_data, get_today_hot_data, get_yesterday_hot_data
from blog.models import Post

def get_week_hot_posts():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    posts = Post.objects \
                .filter(read_details__date__lt=today, read_details__date__gte=date) \
                .values('id', 'title') \
                .annotate(read_num_sum=Sum('read_details__read_num')) \
                .order_by('-read_num_sum')
    return posts[:7]

def get_month_hot_posts():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=30)
    posts = Post.objects \
                .filter(read_details__date__lt=today, read_details__date__gte=date) \
                .values('id', 'title') \
                .annotate(read_num_sum=Sum('read_details__read_num')) \
                .order_by('-read_num_sum')
    return posts[:10]

def statistics(request):
    blog_content_type = ContentType.objects.get_for_model(Post)
    dates, read_nums = get_week_read_data(blog_content_type)

    # 获取一周热门博客的缓存数据
    week_hot_posts = cache.get('week_hot_posts')
    if week_hot_posts is None:
        week_hot_posts = get_week_hot_posts()
        cache.set('week_hot_posts',week_hot_posts,3600)
    # 测试
    #     print('cache')
    # else:
    #     print('use cache')

    # 获取一个月的热门博客缓存数据
    month_hot_posts = cache.get('month_hot_posts')
    if month_hot_posts is None:
        month_hot_posts = get_month_hot_posts()
        cache.set('month_hot_posts',month_hot_posts,3600)

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['week_hot_posts'] = week_hot_posts
    context['month_hot_posts'] = month_hot_posts
    return render(request, 'read_statistics/statistics.html',context)