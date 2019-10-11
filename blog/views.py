import logging

from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.core.paginator import Paginator  # 分页功能
from django.db.models import Count
from .models import BlogType, Blog
from read_statistics.utils import response_cookie_key


logger = logging.getLogger('console')

def get_blog_list_common_data(request, blogs):
    '''获取博客列表共同数据'''
    # 使用分页器对象对博客进行分页，每页显示10条博客，page变量为Paginator的实例对象
    page = Paginator(blogs, settings.EACH_PAGE_BLOGS_NUMBER)
    current_page = request.GET.get('page', 1) # 取出url的page参数
    page_obj = page.get_page(current_page) # page_obj变量是某一页面的具体博客信息对象
    page_num = page_obj.number # 获取当前页的页码 
    # 根据页码来重新生成一个遍历列表，取当前页面+2与-2页：例[1,2,current_page=3,4,5]
    page_list = list(range(max(page_num-2, 1), min(page_num+3, page.num_pages+1)))
    # 添加省略号，例[1,...,5,6,7,8,9,...,12]
    if page_list[0]-2 >= 1:
        page_list.insert(0, '...')
    if page.num_pages - page_list[-1] >= 2:
        page_list.append('...')
    # 页面列表首值与尾值不等于1，总页码值时分别添加1与总页码值，达到[1,2,3,current_page=4,5,6,page.num_pages=12]效果
    if page_list[0] != 1:
        page_list.insert(0, 1)
    if page_list[-1] != page.num_pages:
        page_list.append(page.num_pages)
    # 获取博客所有的分类，并使用annotate备注添加实例属性blog_count，统计各分类有多少篇博客
    blog_types = BlogType.objects.annotate(blog_count=Count('blog'))
    # 按照年月进行日期的分类归档，并统计每个月有多少篇博客
    blog_dates = Blog.objects.dates('created_time', 'month', 'DESC') 
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_dates_dict[blog_date] = Blog.objects.filter(created_time__year=blog_date.year, 
            created_time__month=blog_date.month).count()
    content = {
        'page_obj': page_obj, 'page_list': page_list, 
        'blogs': page_obj.object_list, 'blog_types': blog_types,
        'blog_dates_dict': blog_dates_dict
    }
    return content

def blog_list(request):
    '''博客展示列表'''
    blogs = Blog.objects.all() 
    content = get_blog_list_common_data(request, blogs)
    return render(request, 'blog/blog_list.html', content)


def blogs_with_type(request, blog_type_pk):
    '''博客分类'''
    # 查询博客分类，pk为参数blog_type_pk，得到此对象，如没有引发404异常
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    # 查询博客，条件：分类为blog_type对象，可能会有多条数据，所以使用filter
    blogs = Blog.objects.filter(blog_type=blog_type.pk)
    content = get_blog_list_common_data(request, blogs)
    content['blog_type'] = blog_type
    return render(request, 'blog/blogs_with_type.html', content)


def blogs_with_date(request, year, month):
    # 查询博客，条件：分类为blog_type对象，可能会有多条数据，所以使用filter
    blogs = Blog.objects.filter(created_time__year=year, created_time__month=month)
    content = get_blog_list_common_data(request, blogs)
    content['blog_date_sort'] = '%s年%s月' %(year, month)
    return render(request, 'blog/blogs_with_date.html', content)


def blog_detail(request, blog_pk):
    '''博客详细内容'''
    # 相当于使用Blog.objects.get(pk=blog_pk)，区别是如果查询不到则触发404异常
    blog = get_object_or_404(Blog, pk=blog_pk)
    blog_previous = Blog.objects.filter(pk__gt=blog.pk).last()
    blog_next = Blog.objects.filter(pk__lt=blog_pk).first()
    content = {
        'blog': blog, 'blog_previous': blog_previous, 'blog_next': blog_next
    }
    # 阅读计数判定要求为：访客浏览时只要浏览器不关闭那么重复访问某一篇博客时 阅读计数不重复增加
    key = response_cookie_key(request, blog)
    response = render(request, 'blog/blog_detail.html', content)
    # 得到cookie键，设置cookie，时间为浏览器关闭就失效
    response.set_cookie(key, 'true')
    return response