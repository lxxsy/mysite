from django.contrib import admin
from .models import BlogType, Blog


@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
	# get_read_num是一个方法，获取每篇博客的阅读量，具体可查看ReadNumExpandMethod类查看功能
    list_display = ('id', 'title', 'blog_type', 'get_read_num', 'created_time', 'last_updated_time', 'isdeleted', 'author')