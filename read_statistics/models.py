from django.db import models
from django.db.models.fields import exceptions # 异常集合
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType # 此应用记录了每个创建的模型类，内置应用


# 计数扩展功能类，有模型需要使用计数功能时，即可继承此类
class ReadNumExpandMethod():
	def get_read_num(self):
		try:
			ct = ContentType.objects.get_for_model(self)  # 等同于ct = ContentType.objects.get(model=self) self指类本身
			read_num_obj = ReadNum.objects.get(content_type=ct, object_id=self.pk)
			return read_num_obj.read_num
		except exceptions.ObjectDoesNotExist:
			return 0


# 阅读计数
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = 'readnum'


# 每天阅读计数
class ReadDetail(models.Model):
    date = models.DateField(auto_now_add=True)
    read_num = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = 'readdetail'

