from django.contrib.contenttypes.models import ContentType
from .models import ReadNum

def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)

    # 阅读统计
    if not request.COOKIES.get(key):
        if ReadNum.objects.filter(content_type=ct, object_id=obj).count():
            # 如果存在记录
            readnum = ReadNum.objects.get(content_type=ct, object_id=obj)
        else:
            readnum = ReadNum(content_type=ct, object_id=obj)
        readnum.read_num += 1
        readnum.save()
    return key