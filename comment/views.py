import logging
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from blog.models import Blog
from .models import Comment
from .forms import CommentForm

logger = logging.getLogger('console')

def submit_comment(request):
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    comment_form = CommentForm(request.POST, user=request.user)
    data = {}
    if comment_form.is_valid():
        comment = Comment()
        comment.text = comment_form.cleaned_data['text']
        comment.user = comment_form.cleaned_data['user']
        comment.content_object = comment_form.cleaned_data['content_object']
        parent = comment_form.cleaned_data['parent']
        # 判断是顶级评论还是下级回复
        if not parent is None:
            comment.root = parent if parent.root is None else parent.root
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.get_nickname_or_username()
        data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        data['text'] = comment.text
        # reply_to用于说明回复是回复了哪个用户的，案例admin (2019-10-17 16:38:00) 回复 admin
        if parent is None:
            data['reply_to'] = ''
        else:
            data['reply_to'] = comment.reply_to.get_nickname_or_username()
        data['pk'] = comment.pk
        # root_pk用于回复的内容需要放在顶级评论内容之下，root_pk存放的是顶级评论的主键，
        # 案例$("#"+data['root_pk']).append(reply_html);--><div class="comment" id="{{ comment.pk }}">
        data['root_pk'] = comment.root.pk if not comment.root is None else ''
    else:
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)