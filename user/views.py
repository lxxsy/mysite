import string
import random
import time
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.urls import reverse
from django.http import JsonResponse
from blog.models import Blog
from .forms import SignInForm, SignUpForm, NicknameChangeForm, BindEmailForm
from .models import Profile


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
    return render(request, 'user/sign_in.html', content)


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
    return render(request, 'user/sign_up.html', content)

# 登出处理
def sign_out(request):
    logout(request)
    return redirect(request.GET.get('form'), reverse('home'))

# 个人资料展示
def user_info(request):
    return render(request, 'user/user_info.html')

# 修改昵称
def nickname_change(request):
    redirect_to = request.GET.get('form', reverse('home'))
    if request.method == 'POST':
        nickname_change_form = NicknameChangeForm(request.POST, user=request.user)
        if nickname_change_form.is_valid():
            nickname_new = nickname_change_form.cleaned_data['nickname_new']
            profile_obj, created = Profile.objects.get_or_create(user=request.user)
            profile_obj.nickname = nickname_new
            profile_obj.save()
            return redirect(redirect_to)
    else:
        nickname_change_form = NicknameChangeForm()
    content = {
        'page_title': '修改昵称', 'form': nickname_change_form,
        'submit_text': '修改', 'redirect_to': redirect_to
    }
    return render(request, 'form.html', content)

# 绑定邮箱
def bind_email(request):
    redirect_to = request.GET.get('form', reverse('home'))
    if request.method == 'POST':
        bind_email_form = BindEmailForm(request.POST, request=request)
        if bind_email_form.is_valid():
            email = bind_email_form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            return redirect(redirect_to)
    else:
        bind_email_form = BindEmailForm()
    content = {
        'page_title': '绑定邮箱', 'form': bind_email_form,
        'submit_text': '绑定', 'redirect_to': redirect_to
    }
    return render(request, 'user/verification_code.html', content)

# 发送验证码
def send_verification_code(request):
    email = request.GET.get('email')
    data = {}
    if email != '':
        # 生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 60:
            data['status'] = 'ERROR'
        else:
            request.session['bind_email_code'] = code
            request.session['send_code_time'] = now
            # 发送验证码邮件
            send_mail(
                '绑定邮箱',
                '验证码： %s' % code,
                '443936974@qq.com',
                [email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)
