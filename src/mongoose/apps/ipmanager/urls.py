from django.urls import path, include
from .views import export_intranet_segment
from .views import import_internet_ip_info
from .views import import_intranet_ip_info

urlpatterns = [
    path('export_intranet_segment/', export_intranet_segment),
    path('import_internet_ip_info/', import_internet_ip_info),
    path('import_intranet_ip_info/', import_intranet_ip_info),
]
