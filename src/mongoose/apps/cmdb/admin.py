from django.contrib import admin

from .models import CloudAccount
from .models import Asset
from .models import Service
from .models import NetworkAdapter
from .models import Cpu
from .models import Memory
from .models import Disk
from .models import NetworkDevicePort
from .models import NetworkDeviceVLan
from .models import IDC
from .models import Room
from .models import Cabinet
from .models import Unit
from .models import IP


class CloudAccountAdmin(admin.ModelAdmin):

    list_display = ("name", "cloudName", "accessIp", "status")


class AssetAdmin(admin.ModelAdmin):

    list_display = ("instanceName", "platform", "deviceType", "hostName", )
    exclude = ("other", )   # jsonfield 引起报错


class ServiceAdmin(admin.ModelAdmin):

    list_display = ("name", "domainName")


class NetworkAdapterAdmin(admin.ModelAdmin):

    list_display = ("device", "ip", "front_device", "front_port")


class CpuAdmin(admin.ModelAdmin):

    list_display = ("device", "cpuType", "cpuCoreNum", "rate", "remark")


class MemoryAdmin(admin.ModelAdmin):

    list_display = ("device", "memType", "sn", "size", "manufacturer")


class DiskAdmin(admin.ModelAdmin):

    list_display = ("device", "diskType", "sn", "size", "manufacturer")


class NetworkDevicePortAdmin(admin.ModelAdmin):

    # TODO 补全admin显示内容
    pass


class NetworkDeviceVLanAdmin(admin.ModelAdmin):

    pass


class IdcAdmin(admin.ModelAdmin):

    pass


class RoomAdmin(admin.ModelAdmin):

    pass


class CabinetAdmin(admin.ModelAdmin):

    pass


class UnitAdmin(admin.ModelAdmin):

    pass


class IpAdmin(admin.ModelAdmin):

    pass


admin.site.register(IP, IpAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Cabinet, CabinetAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(IDC, IdcAdmin)
admin.site.register(NetworkDeviceVLan, NetworkDeviceVLanAdmin)
admin.site.register(NetworkDevicePort, NetworkDevicePortAdmin)
admin.site.register(Disk, DiskAdmin)
admin.site.register(Memory, MemoryAdmin)
admin.site.register(Cpu, CpuAdmin)
admin.site.register(NetworkAdapter, NetworkAdapterAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(CloudAccount, CloudAccountAdmin)
