from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField # ckeditor是一个富文本编辑器，将博客的content字段替换为RichTextField
from read_statistics.models import ReadNumExpandMethod # 导入计数统计类，让模型类继承此类
from read_statistics.models import ReadDetail
# from django.contrib.auth.models import User


# 博客类型
class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name

    class Meta:
        db_table = 'blog_type'
        ordering = ['id']


# 博客
class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=50)
    content =RichTextUploadingField()
    blog_type = models.ForeignKey('BlogType', on_delete=models.DO_NOTHING)
    author = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    isdeleted = models.BooleanField(blank=True, default=False)
    read_detail = GenericRelation(ReadDetail)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'blog'
        ordering = ['-id']

