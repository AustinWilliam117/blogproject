import markdown
from django.utils.html import strip_tags
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from read_statistics.models import ReadNumExpandMethod, ReadDetail

class Category(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.name

class Post(models.Model, ReadNumExpandMethod):
    title = models.CharField('标题',max_length=70)
    body = models.TextField('正文')
    read_details = GenericRelation(ReadDetail)
    created_time = models.DateTimeField('创建时间',auto_now=True)
    # 最后一次修改日期
    modified_time = models.DateTimeField('修改时间',auto_now=True)
    excerpt = models.CharField('摘要',max_length=200, blank=True)
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # 首先实例化一个 Markdown 类，用于渲染 body 的文本。
        # 由于摘要并不需要生成文章目录，所以去掉了目录拓展。="ri-arrow-right-s-line" aria-hidden="true"></i>
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

        # 先将 Markdown 文本渲染成 HTML 文本
        # strip_tags 去掉 HTML 文本的全部 HTML 标签
        # 从文本摘取前 50 个字符赋给 excerpt
        self.excerpt = strip_tags(md.convert(self.body))[:200]
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

        ordering = ['-created_time']

    def __str__(self):
        return self.title
