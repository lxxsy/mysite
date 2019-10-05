from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    # http://localhost:8000/blog  进入博客列表
    path('', views.blog_list, name = 'blog_list'),
    # http://localhost:8000/blog/博客的id值  进入博客详情页面
    path('<int:blog_pk>', views.blog_detail, name = 'blog_detail'),
    path('type/<int:blog_type_pk>', views.blogs_with_type, name = 'blogs_with_type'),
]