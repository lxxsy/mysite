import datetime

from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from .models import ReadNum, ReadDetail
from blog.models import Blog

# 设置阅读计数并返回cookie键
def response_cookie_key(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = '%s_%s_read' %(ct.model, obj.pk)
    if not request.COOKIES.get(key):
        '''
        if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
            read_num_obj = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
        else:
            read_num_obj = ReadNum(content_type=ct, object_id=obj.pk)
        '''
        # 等同于上方备注代码块，get_or_create返回一个元组，查询有数据返回数据created为false 无数据新建数据created为true
        read_num_obj, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        read_num_obj.read_num += 1
        read_num_obj.save()
        # 每天阅读计数
        date = timezone.now().date()
        read_detail_obj, created = ReadDetail.objects.get_or_create(date=date, content_type=ct, object_id=obj.pk)
        read_detail_obj.read_num += 1
        read_detail_obj.save()
    return key


def get_seven_days_read_date(ct):
    '''获取每天的阅读计数总和，取7天'''
    current_date = timezone.now().date()
    dates = []
    read_nums = []
    for i in range(7, 0, -1):
        date = current_date - datetime.timedelta(days=i)
        read_detail_obj = ReadDetail.objects.filter(date=date, content_type=ct)
        result = read_detail_obj.aggregate(read_num_sun=Sum('read_num'))
        dates.append(date.strftime('%m/%d'))
        read_nums.append(result['read_num_sun'] or 0)
    return dates, read_nums


# 今日热门博客
def get_today_hot_date(ct):
    current_date = timezone.now().date()
    read_detail_obj = ReadDetail.objects.filter(content_type=ct, date=current_date).order_by('-read_num')
    return read_detail_obj[:7]


# 昨日热门博客
def get_yesterday_hot_date(ct):
    current_date = timezone.now().date()
    yesterday_date = current_date - datetime.timedelta(days=1)
    # blog_obj = Blog.objects.filter(read_detail__date=yesterday_date).order_by('-read_detail__read_num')
    read_detail_obj = ReadDetail.objects.filter(content_type=ct, date=yesterday_date).order_by('-read_num')
    return read_detail_obj[:7]


# 一周热门博客
def get_seven_days_hot_date(ct):
    current_date = timezone.now().date()
    seven_date = current_date - datetime.timedelta(days=7)
    blog_obj = Blog.objects.filter(read_detail__date__lt=current_date, read_detail__date__gte=seven_date) \
                            .values('id', 'title') \
                            .annotate(read_num_sum=Sum('read_detail__read_num')) \
                            .order_by('-read_num_sum')
    return blog_obj[:7]