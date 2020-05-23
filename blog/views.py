import markdown,re
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from .models import Post, Category, Tag
from read_statistics.utils import read_statistics_once_read, get_week_read_data

def get_post_list_comment_data(request,posts):
    # 分页器
    paginator = Paginator(posts, settings.EACH_PAGE_BLOGS_NUMBER)
    page_num = request.GET.get('page', 1)  # 获取url的页面参数（GET请求）
    page_of_posts = paginator.get_page(page_num)
    currentr_page_num = page_of_posts.number  # 获取当前页码
    # 获取当前页码前后各2页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 省略标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 获取日期归档对应的博客数量
    post_dates = Post.objects.dates('created_time', 'month', order="DESC")
    post_dates_dict = {}
    for post_date in post_dates:
        post_count = Post.objects.filter(created_time__year=post_date.year,
                                         created_time__month=post_date.month).count()
        post_dates_dict[post_date] = post_count

    context = {}
    context['posts'] = page_of_posts.object_list
    context['page_of_posts'] = page_of_posts
    context['page_range'] = page_range
    context['categories'] = Category.objects.annotate(post_count=Count('post'))
    context['post_dates'] = post_dates_dict
    context['top10_post_list'] = Post.objects.order_by('-created_time')[0:10]
    return context

def index(request):
    posts= Post.objects.all()
    context = get_post_list_comment_data(request, posts)
    context['category_count'] = Category.objects.all().count()
    context['tag_count'] = Tag.objects.all().count()
    context['date_count'] = Post.objects.dates('created_time', 'month', order="DESC").count()
    return render(request, 'blog/index.html', context)

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    read_cookie_key = read_statistics_once_read(request,post)

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

    context = {}
    context['post'] = post

    # 筛选当前博客大于创建时间的博客最后一条
    context['next_post'] = Post.objects.filter(created_time__gt=post.created_time).last()
    # 筛选当前博客小于创建时间的博客第一条
    context['previous_post'] = Post.objects.filter(created_time__lt=post.created_time).first()
    response = render(request, 'blog/detail.html', context)
    response.set_cookie(read_cookie_key,'true') # 阅读cookie标记
    return response

# 归档
def archive(request, year, month):
    posts = Post.objects.filter(created_time__year=year,
                                created_time__month=month).order_by('-created_time')

    context = get_post_list_comment_data(request, posts)
    context['post_archive'] = '%s年%s月' % (year,month)
    return render(request, 'blog/archive.html', context)

# 分类
def category(request, pk):
    # 记得在开始部分导入 Category 类
    category= get_object_or_404(Category, pk=pk)
    posts = Post.objects.filter(category=category).order_by('-created_time')

    context = get_post_list_comment_data(request, posts)
    context['category'] = category
    return render(request, 'blog/category.html', context)

# 标签
def tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    posts = Post.objects.filter(tags=tag).order_by('-created_time')
    context = get_post_list_comment_data(request, posts)
    return render(request, 'blog/category.html', context)

# 统计
def statistics(request):
    post_content_type = ContentType.objects.get_for_model(Post)
    dates, read_nums = get_week_read_data(post_content_type)
    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    return render(request, 'read_statistics/statistics.html', context)




