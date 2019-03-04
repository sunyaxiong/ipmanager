from IPy import IP

from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib import messages
from django.contrib.auth.models import User

from .models import IntranetIp
from .models import InternetIP


@receiver(post_save, sender="ipmanager.IntranetSegment")
def auto_create_ip(sender, instance, created, *args, **kwargs):
    """
    网段创建成功后，自动创建IP地址
    :param sender:
    :param instance:
    :param created:
    :param args:
    :param kwargs:
    :return:
    """
    ip_segment = IP(instance.netId).make_net(instance.mask)
    ip_list = []
    is_ip_exists = IntranetIp.objects.filter(ip=instance.netId, mask=instance.mask)
    if not is_ip_exists:
        for ip in IP(ip_segment):
            ip_instance = IntranetIp(ip=ip.strNormal(), mask=instance.mask, netSegment=instance)
            ip_list.append(ip_instance)

        # print(ip_list)
        IntranetIp.objects.bulk_create(ip_list)
    return None


@receiver(post_save, sender="ipmanager.InternetSegment")
def auto_create_internet_ip(sender, instance, created, *args, **kwargs):
    """
    自动创建互联网IP
    :param sender:
    :param instance: 互联网IP段
    :param created:
    :param args:
    :param kwargs:
    :return:
    """
    ip_segment = IP(instance.address).make_net(instance.mask)
    ip_list = []
    is_ip_exists = InternetIP.objects.filter(ip=instance.address)
    if not is_ip_exists:
        for ip in IP(ip_segment):
            ip_instance = InternetIP(ip=ip.strNormal(), ipNet=instance, useFor="auto")
            ip_list.append(ip_instance)

        # print(ip_list)
        InternetIP.objects.bulk_create(ip_list)
    return None
