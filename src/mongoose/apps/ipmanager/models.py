from IPy import IP

from django.db import models
from django.contrib import messages
from django.core import exceptions

from lib.models import BaseModel
from django.contrib.auth.models import User
from . import choices


class Zone(BaseModel):
    """
    区域管理
    # 因多网段可能属于同一逻辑区域，所以将区域定义抽出
    """
    name = models.CharField("区域名称", max_length=128)
    grade = models.IntegerField("区域等级", default=0, choices=choices.ZONE_CHOICES)
    mask = models.IntegerField("掩码", null=True, blank=True)
    fatherZone = models.ForeignKey(
        "self", verbose_name="父区域", on_delete=None, null=True, blank=True, db_constraint=False
    )
    netId = models.GenericIPAddressField("网络号", null=True, blank=True)
    admin = models.ForeignKey(User, verbose_name="管理员", on_delete=None, null=True, blank=True, db_constraint=False)
    addressRange = models.CharField("地址范围", max_length=128, null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # 区域等级，自动赋值
        if self.fatherZone:
            self.grade = 1

        # 地址范围计算
        ip_segment = "{}/{}".format(self.netId, self.mask)
        self.addressRange = IP(ip_segment).strNormal(3)

        super(self.__class__, self).save()

    class Meta:
        verbose_name_plural = "区域管理"
        verbose_name = "区域"

    def __str__(self):
        _name = self.name
        try:
            if self.grade == 0:
                _name = "{}({}/{})".format(self.name, self.netId, self.mask)
            if self.grade == 1:
                _name = "{}--{}({}/{})".format(self.fatherZone, self.name, self.netId, self.mask)
            if self.grade == 2:
                _name = "{}--{}--{}({}/{})".format(
                    self.fatherZone.fatherZone, self.fatherZone, self.name, self.netId, self.mask
                )
        except Exception as e:
            _name = "////"
        return _name


class Customer(BaseModel):

    name = models.CharField("用户姓名", max_length=128)
    phone = models.CharField("用户电话", max_length=128, null=True, blank=True)
    email = models.EmailField("用户邮箱", null=True, blank=True)
    department = models.CharField("部门", max_length=128, null=True, blank=True)
    job = models.CharField("岗位", max_length=128, null=True, blank=True)

    class Meta:
        verbose_name_plural = "客户管理"
        verbose_name = "客户"

    def __str__(self):
        return self.name


class IntranetSegment(BaseModel):
    """
    内网IP规划表
    """
    netId = models.GenericIPAddressField("子网")
    mask = models.IntegerField("掩码")
    zone = models.ForeignKey(Zone, verbose_name="区域", on_delete=None, null=True, blank=True, db_constraint=False)
    addressRange = models.CharField("地址范围", max_length=128, null=True, blank=True)
    service = models.CharField("支撑的服务器", max_length=128, null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        # 地址范围计算
        ip_segment = "{}/{}".format(self.netId, self.mask)
        self.addressRange = IP(ip_segment).strNormal(3)

        super(IntranetSegment, self).save()

    class Meta:
        verbose_name_plural = "内网IP段规划"
        verbose_name = "网段"

    def __str__(self):
        try:
            _name = "{}:{}/{}".format(self.zone.name, self.netId, self.mask)
        except Exception as e:
            _name = "{}:{}/{}".format(self.zone, self.netId, self.mask)
        return _name


class Vlan(BaseModel):
    """
    vlan 表
    """
    vlanID = models.IntegerField("vlanID")
    vlanName = models.CharField("vlan名称", max_length=128)
    netSegment = models.ForeignKey(IntranetSegment, on_delete=None, null=True, blank=True, db_constraint=False)
    remark = models.CharField("备注", max_length=256, null=True, blank=True)
    statue = models.IntegerField("状态", default=0)

    class Meta:
        verbose_name_plural = "vlan管理"
        verbose_name = "vlan"

    def __str__(self):
        return "{}-{}".format(self.vlanID, self.vlanName)


class IntranetIp(BaseModel):
    """
    内网IP
    """
    ip = models.GenericIPAddressField("ip地址")
    mask = models.IntegerField("掩码")
    hostname = models.CharField("主机名", null=True, blank=True, max_length=128)
    netSegment = models.ForeignKey(
        IntranetSegment, verbose_name="内网段", on_delete=None, null=True, blank=True, db_constraint=False
    )
    customer = models.ForeignKey(Customer, on_delete=None, null=True, blank=True, db_constraint=False)
    proposer = models.ForeignKey(User, on_delete=None, null=True, blank=True, db_constraint=False)
    status = models.IntegerField("状态", default=0, choices=choices.IP_STATUS)
    desc = models.CharField("描述", null=True, blank=True, max_length=256)
    appName = models.CharField("应用名称", max_length=256, null=True, blank=True)
    proposerTime = models.DateTimeField("申请时间", null=True, blank=True)
    expireTime = models.DateTimeField("到期时间", null=True, blank=True)

    class Meta:
        verbose_name_plural = "内网IP"
        verbose_name = "内网IP"
        unique_together = ("ip", "mask")

    def __str__(self):
        return self.ip


class InternetSegment(BaseModel):
    """
    互联网IP段管理
    """
    serviceProvider = models.CharField("服务商", max_length=128)
    netNumber = models.IntegerField("网段序号")
    address = models.GenericIPAddressField("地址段")
    mask = models.IntegerField("掩码")

    class Meta:
        verbose_name_plural = "互联网IP段"
        verbose_name = "互联网IP段"

    def __str__(self):
        return "{}-{}".format(self.serviceProvider, self.netNumber)


class InternetIP(BaseModel):
    """
    互联网IP管理
    """
    ip = models.GenericIPAddressField("ip")
    ipNet = models.ForeignKey(InternetSegment, on_delete=None, db_constraint=False)
    status = models.IntegerField("状态", default=0)
    reserved = models.IntegerField("预留", default=0)
    allocationTime = models.DateTimeField("分配时间", null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=None, db_constraint=False, null=True, blank=True)
    useFor = models.TextField("用途", max_length=256)
    businessType = models.IntegerField("业务类型", null=True, blank=True, choices=choices.BUSINESS_TYPE)
    remark = models.CharField("备注", max_length=256, null=True, blank=True)
    networkDevice = models.BooleanField("是否网络设备", default=0)

    class Meta:
        verbose_name_plural = "互联网IP"
        verbose_name = "互联网IP"

    def __str__(self):
        return self.ip


class Demo1(BaseModel):
    name = models.CharField("名称", max_length=128, null=True, blank=True)


class Demo2(BaseModel):
    desc = models.CharField("描述", max_length=128, null=True, blank=True)
    fk = models.ForeignKey(Demo1, on_delete=None, db_constraint=False)


from .signals import auto_create_ip
from .signals import auto_create_internet_ip
