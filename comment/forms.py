from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions
from ckeditor.widgets import CKEditorWidget
from blog.models import Blog
from .models import Comment


class CommentForm(forms.Form):
    text = forms.CharField(label=False, widget=CKEditorWidget(config_name='comment_ckeditor'), error_messages={'required': '评论内容不能为空'})
    content_type = forms.CharField(widget=forms.HiddenInput())
    object_id = forms.IntegerField(widget=forms.HiddenInput())
    reply_comment_pk = forms.IntegerField(widget=forms.HiddenInput())
    '''
        判断用户是否登录，通过request.user 但此表单类没有request对象，
        通过comment_form = CommentForm(request.POST, user=request.user)将user传递过来
        表单类默认需要调用父类的初始化方法，父类初始化不需要自己设置的参数，这里需要提取出来
    '''
    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户未登录')
        content_type = self.cleaned_data.get('content_type')
        object_id = self.cleaned_data.get('object_id')
        try:
            model_class = ContentType.objects.get(model=content_type).model_class()
            model_obj = model_class.objects.filter(pk=object_id)[0]
            self.cleaned_data['content_object'] = model_obj
        except exceptions.ObjectDoesNotExist:
             raise forms.ValidationError('评论对象不存在')
        return self.cleaned_data

    def clean_reply_comment_pk(self):
        reply_comment_pk = self.cleaned_data['reply_comment_pk']
        if reply_comment_pk < 0:
            return forms.ValidationError('评论异常')
        elif reply_comment_pk == 0:
            self.cleaned_data['parent'] = None
        elif Comment.objects.filter(pk=reply_comment_pk).exists():
            self.cleaned_data['parent'] = Comment.objects.get(pk=reply_comment_pk)
        else:
            return forms.ValidationError('回复异常')
        return reply_comment_pk
