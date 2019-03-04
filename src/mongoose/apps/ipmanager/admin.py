from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages

from . import models
from . import filters
from . import forms


@admin.register(models.Zone)
class ZoneAdmin(admin.ModelAdmin):
    form = forms.ZoneForm
    list_display = (
        "name", "netId", "mask", "fatherZone", "grade", "admin", "_ip_segment_list_href"
    )
    list_filter = ("grade", )
    readonly_fields = ("grade", )

    def _ip_segment_list_href(self, instance):
        """
        区域跳转到IP段列表
        :param instance:
        :return:
        """
        return format_html(
            '<a href="/admin/ipmanager/intranetsegment/?zone__id={}">{}</a>'.format(
                instance.id, instance.addressRange
            )
        )
    _ip_segment_list_href.short_description = "子网列表"

    # def save_model(self, request, obj, form, change):
    #     ip_segment = "{}/{}".format(obj.netId, obj.mask)
    #     father_ip_segment = "{}/{}".format(obj.fatherZone.netId, obj.fatherZone.mask)
    #     if ip_segment not in father_ip_segment:
    #         return messages.warning(request, "该子网不属于上级分组")
    #     obj.save()


class CustomerAdmin(admin.ModelAdmin):
    pass


class IntranetSegmentAdmin(admin.ModelAdmin):
    """
    内网网段admin样式
    """

    list_display = ("_subnet", "zone", "service", "_ip_list_href")
    list_filter = ("service", "zone")
    search_fields = ("netId", )

    def _subnet(self, instance):
        return "{}/{}".format(instance.netId, instance.mask)

    def _zone(self, instance):
        # TODO 确定网段列表页区域显示名称，当前完全根据zone来确定显示名称；2级子网无zone的显示其父级子网zone名称

        if instance.grade == 0:
            return instance.zone
        elif instance.grade == 1:
            return instance.zone
        # elif instance.grade == 2:
        #     IP段列表页区域显示：顶级区域+一级区域+* ，原则上二级子网不维护区域名称
            # __name = instance.fatherSubnet.zone if instance.fatherSubnet else "!!"
            # return "{}-*".format(__name)

    def _ip_list_href(self, instance):
        """
        IP段跳转到IP列表页
        :param instance:
        :return:
        """
        return format_html(
            '<a href="/admin/ipmanager/intranetip/?netSegment__id={}">{}</a>'.format(
                instance.id, instance.addressRange
            )
        )
    _ip_list_href.short_description = "地址范围"


class VlanAdmin(admin.ModelAdmin):
    list_display = ("vlanID", "vlanName", "remark")


class IntranetIpAdmin(admin.ModelAdmin):
    """
    内网IP admin样式
    """
    date_hierarchy = "dt_created"
    list_display = (
        "ip", "mask", "hostname", "netSegment", "customer", "proposer", "_status", "appName", "proposerTime",
        "expireTime", "desc"
    )
    list_filter = ("status", filters.ZoneFilter, "netSegment")
    search_fields = ("ip", "desc")

    def _zone(self, instance):

        zone_name = "/"
        if not instance.netSegment.grade:
            zone_name = instance.netSegment.zone
        elif instance.netSegment.grade == 1:
            # zone_name = "{}-{}".format(
            #     instance.netSegment.zone.fatherZone.name, instance.netSegment.zone.name
            # )
            zone_name = instance.netSegment.zone
        elif instance.netSegment.grade == 2:
            zone_name = "{}-{}".format(
                instance.netSegment.fatherSubnet.zone, "*"
            )

        return zone_name

    def _status(self, instance):
        if instance.status:
            color = "green"
        else:
            color = "red"
        return format_html(
            '<span style="background: {}; color: white">{}</span>', color, instance.get_status_display()
        )


class InternetSegmentAdmin(admin.ModelAdmin):
    """
    互联网段 admin样式
    """
    list_display = ("__str__", "serviceProvider", "netNumber", "address", "mask")
    list_filter = ("serviceProvider", )


class InternetIpAdmin(admin.ModelAdmin):
    """
    互联网IP admin样式
    """
    list_display = ("__str__", "ipNet", "useFor")
    list_filter = ("ipNet", )
    search_fields = ("ip", )


admin.site.register(models.InternetIP, InternetIpAdmin)
admin.site.register(models.InternetSegment, InternetSegmentAdmin)

admin.site.register(models.IntranetIp, IntranetIpAdmin)
admin.site.register(models.Vlan, VlanAdmin)
admin.site.register(models.IntranetSegment, IntranetSegmentAdmin)

admin.site.register(models.Customer, CustomerAdmin)
