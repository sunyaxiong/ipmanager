# choices

# CloudAccount表
CLOUD_ACCOUNT_STATUS = (
    (1, "启用"),
    (0, "禁用")
)

CLOUD_ACCOUNT_TYPE = (
    ("vsphere", "vSphere"),
    ("aws", "aws")
)

# Asset表

DEVICE_TYPE = (
    ("vm", "虚拟机"),
    ("phy", "物理机"),
    ("network", "网络设备"),
)
