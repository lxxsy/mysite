from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from ..forms import CommentForm

register = template.Library()

# 制作单篇博客评论总数标签
@register.simple_tag
def get_comment_count(obj):
    ct = ContentType.objects.get_for_model(obj)
    comment_count = Comment.objects.filter(content_type=ct, object_id=obj.pk).count()
    return comment_count

# 制作创建评论表单实例标签
@register.simple_tag
def init_comment_form(obj):
    ct = ContentType.objects.get_for_model(obj)
    form = CommentForm(initial={'content_type': ct.model, 'object_id': obj.pk, 'reply_comment_pk': 0})
    return form

# 制作单篇博客下所有的评论数据标签
@register.simple_tag
def get_comment_obj_list(obj):
    ct = ContentType.objects.get_for_model(obj)
    comment_obj_list = Comment.objects.filter(content_type=ct, object_id=obj.pk, parent=None)
    return comment_obj_list