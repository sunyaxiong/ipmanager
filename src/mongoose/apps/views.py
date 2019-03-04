import sys
import os
import django


sys.path.append('D:\workspace\Mongoose_Proj\mongoose\src\mongoose')  # 将项目路径添加到系统搜寻路径当中
os.environ['DJANGO_SETTINGS_MODULE'] = 'mongoose.settings'  # 设置项目的配置文件
django.setup()
from apps.ipmanager.models import IntranetSegment

IntranetSegment.objects.filter()