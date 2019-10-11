import logging

from django.contrib.auth import authenticate, login
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from blog.models import Blog
from read_statistics.utils import get_seven_days_read_date, get_today_hot_date, get_yesterday_hot_date, get_seven_days_hot_date


logger = logging.getLogger('console')

def index(request):
    ct = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_date(ct)
    today_hot_blogs = get_today_hot_date(ct)
    yesterday_hot_blogs = get_yesterday_hot_date(ct)
    seven_hot_blogs = get_seven_days_hot_date(ct)
    content = {
        'dates': dates, 'read_nums': read_nums,
        'today_hot_blogs': today_hot_blogs, 'yesterday_hot_blogs': yesterday_hot_blogs,
        'seven_hot_blogs': seven_hot_blogs
    }
    return render(request, 'index.html', content)


def sign_in(request):
    username = request.POST.get('username', '')
    pwd = request.POST.get('pwd', '')
    user = authenticate(request, username=username, password=pwd)
    if user is not None:
        login(request, user)
        return redirect('/')
    else:
        return render(request, 'error.html', {'error_message': '用户名或密码不正确'})