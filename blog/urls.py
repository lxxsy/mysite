from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    # http://localhost:8000/blog?page=1  进入博客列表,默认进入第一页
    path('', views.blog_list, name = 'blog_list'),
    # http://localhost:8000/blog/博客的id值  进入博客详情页面
    path('<int:blog_pk>', views.blog_detail, name = 'blog_detail'),
    # http://localhost:8000/blog/type/博客分类的id 按照博客分类对博客进行分类
    path('type/<int:blog_type_pk>', views.blogs_with_type, name = 'blogs_with_type'),
    # http://localhost:8000/blog/date/年/月 按照年月对博客进行归档
    path('date/<int:year>/<int:month>', views.blogs_with_date, name = 'blogs_with_date'),
]