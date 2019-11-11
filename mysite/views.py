import logging

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.urls import reverse
from blog.models import Blog
from read_statistics.utils import get_seven_days_read_date, get_today_hot_date, get_yesterday_hot_date, get_seven_days_hot_date
# from .forms import SignInForm, SignUpForm


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

'''
# 登录处理
def sign_in(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request 创建一个表单实例并用来自请求的数据填充它:
        sign_in_form = SignInForm(request.POST)
        # check whether it's valid 检查它是否有效:
        if sign_in_form.is_valid():
            # 存在则提取用户信息
            user = sign_in_form.cleaned_data.get('user')
            # 用户存在则使用login()进行登录
            login(request, user)
            return redirect(request.GET.get('form', reverse('home')))
    else:
        sign_in_form = SignInForm()
    content = {
        'sign_in_form': sign_in_form
    }
    return render(request, 'sign_in.html', content)


# 注册处理
def sign_up(request):
    if request.method == 'POST':
        sign_up_form = SignUpForm(request.POST)
        if sign_up_form.is_valid():
            username = sign_up_form.cleaned_data.get('username')
            email = sign_up_form.cleaned_data.get('email')
            password = sign_up_form.cleaned_data.get('password')
            # 创建用户，内置User保存密码时需要加密，调用set_password方法即可
            user = User.objects.create_user(username, email, password)
            user.save()
            # 登录
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(request.GET.get('form'), reverse('home'))
    else:
        sign_up_form = SignUpForm()
    content = {
        'sign_up_form': sign_up_form
    }
    return render(request, 'sign_up.html', content)
'''