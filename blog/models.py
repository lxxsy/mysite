from django.db import models
# from django.contrib.auth.models import User


# 博客类型
class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name

    class Meta:
        db_table = 'blog_type'

# 博客
class Blog(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    blog_type = models.ForeignKey('BlogType', on_delete=models.DO_NOTHING)
    author = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    isdeleted = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'blog'


