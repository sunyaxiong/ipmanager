import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import IntranetSegment
from .models import InternetIP
from .models import Customer
from .models import IntranetIp


@csrf_exempt
def export_zone(request):
    if request.method == "GET":
        return HttpResponse("this is Zone import API")
    elif request.method == "POST":
        data = json.loads(request.POST["data"])

        return HttpResponse("Success")


@csrf_exempt
def export_intranet_segment(request):
    if request.method == "GET":
        return HttpResponse("this is IntranetSegment import API")
    elif request.method == "POST":
        segment_list = json.loads(request.POST["data"])
        segment_bulk_list = []
        for i in segment_list:
            if len(i) == 2:
                segment_bulk_list.append(IntranetSegment(netId=i[0], mask=i[1]))
        IntranetSegment.objects.bulk_create(segment_bulk_list)
        all_segment = IntranetSegment.objects.all()
        # TODO 网段创建成功后与区域进行关联: 通过IPy判断是否为二级区域子网,并建立fk关系

        # 手动触发一次网段的save()操作,触发IP创建的信号
        for seg in all_segment:
            seg.save()
        return HttpResponse("ok")


@csrf_exempt
def import_intranet_ip_info(request):
    if request.method == "GET":
        return HttpResponse("this is API for IntranetIP import")
    elif request.method == "POST":
        intranet_ip_info_list = json.loads(request.POST["data"])
        print("views: ", intranet_ip_info_list)
        for i in intranet_ip_info_list:
            customer = None
            if i["Proposer"]:
                if len(i["Proposer"].split(" ")) == 2:
                    name = i["Proposer"].split(" ")
                    customer, has_created = Customer.objects.get_or_create(name=name[0])
                    customer.phone = name[1]
                    customer.save()
                else:
                    customer, has_created = Customer.objects.get_or_create(name=i["Proposer"])
            try:
                ip_instance = IntranetIp.objects.get(ip=i["IP"])
                ip_instance.mask = 24
                ip_instance.hostname = i["hostname"]
                ip_instance.customer = customer
                ip_instance.status = 1
                ip_instance.desc = i["Description"]
                ip_instance.appName = i["APP Name"]
                ip_instance.save()
            except Exception as e:
                print(e, i)

        return HttpResponse("Success")


@csrf_exempt
def import_internet_ip_info(request):
    if request.method == "GET":
        return HttpResponse("this is API for InternetIP import")
    elif request.method == "POST":
        internet_ip_info_list = json.loads(request.POST["data"])
        for i in internet_ip_info_list:
            customer = None
            if i["Proposer"]:
                if len(i["Proposer"].split(" ")) == 2:
                    name = i["Proposer"].split(" ")
                    customer, has_created = Customer.objects.get_or_create(name=name[0])
                    customer.phone = name[1]
                    customer.save()
                else:
                    customer, has_created = Customer.objects.get_or_create(name=i["Proposer"])
            try:
                # print(i["外联网IP"], type(i["外联网IP"]))
                ip_instance = InternetIP.objects.get(ip=i["外联网IP"])
                ip_instance.status = 1 if i["已使用"] == "TRUE" else 0
                ip_instance.customer = customer
                ip_instance.useFor = i["用途"]
                ip_instance.businessType = 1 if i["P（生产）/T（测试）"] == "P" else 0
                ip_instance.remark = i["备注"]
                ip_instance.networkDevice = 1 if i["网络设备"] == "Y" else 0
                ip_instance.save()
            except Exception as e:
                print(e, i)
        return HttpResponse("Success")

