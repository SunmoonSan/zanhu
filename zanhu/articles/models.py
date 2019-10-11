from django.conf import settings
from django.db import models
from django.db.models import CharField, ForeignKey, ImageField, SlugField, TextField, BooleanField, DateTimeField
from slugify import slugify
from taggit.managers import TaggableManager


class ArticleQuerySet(models.query.QuerySet):

    def get_published(self):
        """获取已发表的文字"""
        return self.filter(status="P")

    def get_drafts(self):
        """获取草稿箱的文字"""
        return self.filter(status="D")

    def get_counted_tags(self):
        """统计所有已发表的文章中, 每个标签的数量大于0的"""
        tag_dict = {}
        query = self.get_published().annotate(tagged=models.Count("tags")).filter(tags__gt=0)
        for obj in query:
            for tag in obj.tags.names():
                if tag not in tag_dict:
                    tag_dict[tag] = 1
                else:
                    tag_dict[tag] += 1
        return tag_dict.items()


class Article(models.Model):
    STATUS = (('D', 'Draft'), ('P', 'Published'))
    title = CharField(max_length=255, null=False, unique=True, verbose_name='标题')
    user = ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='author', on_delete=models.SET_NULL,
                      verbose_name='作者')
    image = ImageField(upload_to="articles_pictures/%Y/%m/%d/", verbose_name='文章图片')
    slug = SlugField(max_length=80, null=True, blank=True, verbose_name='(URL)别名')
    status = CharField(max_length=1, choices=STATUS, default='D', verbose_name='状态')
    content = TextField(verbose_name='内容')
    edited = BooleanField(default=False, verbose_name='是否可编辑')
    tags = TaggableManager(help_text='多个标签, 使用逗号隔开')

    created_at = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = DateTimeField(auto_now=True, verbose_name='更新时间')

    objects = ArticleQuerySet.as_manager()

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ("created_at",)

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_field=None):
        self.slug = slugify(self.title)
        super(Article, self).save()
