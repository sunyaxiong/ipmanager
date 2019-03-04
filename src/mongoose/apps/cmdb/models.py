import jsonfield

from django.db import models

from lib.models import BaseModel
from .choices import *


class CloudAccount(BaseModel):
    """
    云账号
    """
    name = models.CharField("名称", max_length=128)
    cloudName = models.CharField("平台类型", max_length=128, choices=CLOUD_ACCOUNT_TYPE)
    accessIp = models.GenericIPAddressField("接入IP")
    status = models.BooleanField("状态", default=0, choices=CLOUD_ACCOUNT_STATUS)

    class Meta:
        verbose_name = "云账户管理"
        verbose_name_plural = "云账户管理"

    def __str__(self):
        return self.name


class Asset(BaseModel):
    """
    虚拟机表，即各个异构云环境下虚拟机实例
    """
    instanceName = models.CharField("实例名称", max_length=128, unique=True)
    hostName = models.CharField("计算机名称", max_length=128)
    deviceType = models.CharField("实例类型", max_length=128, choices=DEVICE_TYPE, null=True, blank=True)
    platform = models.CharField("平台", max_length=128, choices=CLOUD_ACCOUNT_TYPE, default=0)
    isPhysical = models.BooleanField("是否物理资源", default=0)
    localIp = models.GenericIPAddressField("私有IP", null=True, blank=True)
    manageIp = models.GenericIPAddressField("管理IP")
    publicIp = models.GenericIPAddressField("公网IP", null=True, blank=True)
    os = models.CharField("操作系统", max_length=128, null=True, blank=True)
    RAID = models.CharField("RAID", max_length=128, null=True, blank=True)
    manager = models.CharField("管理员", max_length=128)
    other = jsonfield.JSONField("其它信息", null=True, blank=True)
    des = models.CharField("备注", max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = "资源管理"
        verbose_name_plural = "资源管理"

    def __str__(self):
        return "{}-{}".format(self.instanceName, self.hostName)


class Service(BaseModel):
    """
    服务名称管理
    """
    name = models.CharField("服务名称", max_length=128)
    domainName = models.CharField("域名", max_length=128)
    serverOn = models.ManyToManyField(Asset, max_length=128)

    class Meta:
        verbose_name = "服务名称管理"
        verbose_name_plural = "服务名称管理"

    def __str__(self):
        return self.name


class NetworkAdapter(BaseModel):
    """
    网卡表: 虚拟机、物理机
    """
    device = models.ForeignKey(Asset, verbose_name="关联设备", on_delete=None)
    ip = models.GenericIPAddressField("IP地址")
    front_device = models.CharField("上联设备", max_length=128)
    front_port = models.CharField("上联口", max_length=128)
    port_state = models.CharField("端口状态", max_length=128)
    remote_manage = models.CharField("远程管理卡状态", max_length=128)
    remark = models.TextField("备注")

    class Meta:
        verbose_name = "网卡管理"
        verbose_name_plural = "网卡管理"

    def __str__(self):
        return self.device.hostName


class Cpu(BaseModel):
    """
    cpu 表
    """
    device = models.ForeignKey(Asset, verbose_name="关联设备", on_delete=None)
    cpuType = models.CharField("cpu型号", max_length=128)
    cpuCoreNum = models.IntegerField("核心数")
    rate = models.CharField("主频", max_length=128)
    remark = models.TextField("备注")

    class Meta:
        verbose_name = "CPU管理"
        verbose_name_plural = "CPU管理"

    def __str__(self):
        return self.device.hostName


class Memory(BaseModel):
    """
    内存表
    """
    device = models.ForeignKey(Asset, verbose_name="关联设备", on_delete=None)
    memType = models.CharField("内存型号", max_length=128)
    sn = models.CharField("SN号", max_length=128)
    size = models.CharField("容量", max_length=128)
    manufacturer = models.CharField("厂家", max_length=128)
    remark = models.TextField("备注")

    class Meta:
        verbose_name = "内存管理"
        verbose_name_plural = "内存管理"

    def __str__(self):
        return self.device.hostName


class Disk(BaseModel):
    """
    磁盘表
    """
    device = models.ForeignKey(Asset, verbose_name="关联设备", on_delete=None)
    diskType = models.CharField("磁盘型号", max_length=128)
    sn = models.CharField("SN号", max_length=128)
    size = models.CharField("容量", max_length=128)
    interfaceType = models.CharField("接口类型", max_length=128)
    manufacturer = models.CharField("厂商", max_length=128)
    remark = models.TextField("备注")

    class Meta:
        verbose_name = "磁盘管理"
        verbose_name_plural = "磁盘管理"

    def __str__(self):
        return self.device.hostName


class NetworkDevice(BaseModel):
    """
    网络设备表，虚拟网络设备及物理设备
    """
    pass


class NetworkDevicePort(BaseModel):
    """
    网络设备端口表
    """
    device = models.ForeignKey(NetworkDevice, verbose_name="关联设备", on_delete=None)
    vlanId = models.CharField("vlanID", max_length=128)
    portState = models.CharField("端口状态", max_length=128)
    connectedDevice = models.ForeignKey(Asset, max_length=128, on_delete=None)
    port_num = models.CharField("端口号", max_length=128)

    class Meta:
        verbose_name_plural = "网络设备端口管理"
        verbose_name = "网络设备端口管理"

    def __str__(self):
        return self.port_num


class NetworkDeviceVLan(BaseModel):
    """
    网络设备vlan划分
    """
    device = models.ForeignKey(NetworkDevice, verbose_name="关联设备", on_delete=None)
    vlanNo = models.CharField("vlan号", max_length=128)
    vlanif = models.CharField("vlanif", max_length=128)

    class Meta:
        verbose_name = "vLan管理"
        verbose_name_plural = "vLan管理"

    def __str__(self):
        return self.vlanif


class IDC(BaseModel):
    """
    机房表
    """
    name = models.CharField("机房名称", max_length=128)
    address = models.CharField("地址", max_length=128)
    phone = models.CharField("联系电话", max_length=128)
    vendor = models.CharField("服务商", max_length=128)

    class Meta:
        verbose_name_plural = "IDC管理"
        verbose_name = "IDC管理"

    def __str__(self):
        return self.name


class Room(BaseModel):
    """
    机房房间表
    """
    num = models.CharField("房间号", max_length=128)
    desc = models.CharField("描述", max_length=128)
    idc = models.ForeignKey(IDC, on_delete=None)

    class Meta:
        verbose_name_plural = "IDC房间管理"
        verbose_name = "IDC房间管理"

    def __str__(self):
        return self.num


class Cabinet(BaseModel):
    """
    机柜表
    """
    num = models.CharField("机柜号", max_length=128)
    height = models.IntegerField("总U数")
    root = models.ForeignKey(Room, on_delete=None)

    class Meta:
        verbose_name = "IDC机柜管理"
        verbose_name_plural = "IDC机柜管理"

    def __str__(self):
        return self.num


class Unit(BaseModel):
    """
    U 位
    """
    num = models.IntegerField("U位")
    cabinet = models.ForeignKey(Cabinet, on_delete=None)

    class Meta:
        verbose_name = "U位管理"
        verbose_name_plural = "U位管理"

    def __str__(self):
        return self.num


class IP(BaseModel):
    """
    IP 管理
    """
    ipAddress = models.GenericIPAddressField("IP")
    isInternet = models.BooleanField("是否互联网IP", default=1)
    asset = models.ForeignKey(Asset, on_delete=None)
    status = models.BooleanField("状态", default=0)

    class Meta:
        verbose_name_plural = "互联网IP管理"
        verbose_name = "互联网IP管理"

    def __str__(self):
        return self.ipAddress
