from django.shortcuts import render, get_object_or_404
from .models import BlogType, Blog


def blog_list(request):
    '''博客展示列表'''
    # 获取所有博客
    blogs = Blog.objects.all()
    # 博客列表与博客总数通过上下文传递给模板
    content = {
        'blogs': blogs, 'blogs_count': blogs.count()
    }
    return render(request, 'blog/blog_list.html', content)

def blog_detail(request, blog_pk):
    '''博客详细内容'''
    # 相当于使用Blog.objects.get(pk=blog_pk)，不过区别是如果查询不到则触发404异常
    blog = get_object_or_404(Blog, pk=blog_pk)
    content = {
        'blog': blog
    }
    return render(request, 'blog/blog_detail.html', content)

def blogs_with_type(request, blog_type_pk):
    '''博客分类'''
    # 查询博客分类，pk为参数blog_type_pk，得到此对象，如没有引发404异常
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    # 查询博客，条件：分类为blog_type对象，可能会有多条数据，所以使用filter
    blog_list = Blog.objects.filter(blog_type=blog_type.pk)
    # blog_list:对象列表 blog_type:单个对象
    content = {
        'blog_list': blog_list, 'blog_type': blog_type
    }
    return render(request, 'blog/blogs_with_type.html', content)