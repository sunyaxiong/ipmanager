from IPy import IP

from django import forms
from django.forms import ValidationError

from .models import Zone


class ZoneForm(forms.ModelForm):

    class Meta:
        model = Zone
        fields = "__all__"

    def clean(self):
        return self.cleaned_data

    def clean_netId(self):
        # 此处校验字段，并返回提示信息
        if self.cleaned_data["fatherZone"]:
            try:
                ip_segment = "{}/{}".format(self.cleaned_data["netId"], self.cleaned_data["mask"])
                father_segment = "{}/{}".format(
                    self.cleaned_data["fatherZone"].netId, self.cleaned_data["fatherZone"].mask
                )
                if IP(ip_segment) not in IP(father_segment):
                    raise ValidationError("该子网不存在父级子网中")
            except Exception as e:
                raise ValidationError(e)
        return self.cleaned_data["netId"]
    # def clean(self):
    #     print(self.cleaned_data)

