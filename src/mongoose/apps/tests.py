import sys
import os
import pprint
import django
import xlrd
from xlrd import XL_CELL_NUMBER
import requests
import json
from lib.excel import Excel


if __name__ == "__main__":

    """
    导入策略:
        1 不对区域进行导入,包括一级区域和二级区域,针对区域数据进行手动录入
        2 
    """

    # 导入intranetIP 信息
    excel = Excel("iplist.xlsx")
    for sheet in excel.wb.sheets()[1:]:
        data = excel.load_sheet_content(sheet.number)
        in_use_data = [i for i in data if i["status"] == "in use"]
        print("in use: ", in_use_data)
        res = requests.post("http://127.0.0.1:8080/ip/import_intranet_ip_info/", data={"data": json.dumps(in_use_data)})
        print(f"sheet表{res.ok}: {sheet.name} 完成")

    # 导入InternetIP 信息
    # excel = Excel("iplist-bak.xlsx")
    # dianxin_sheet = excel.wb.sheet_by_name("网通")
    # data = excel.load_sheet_content(dianxin_sheet.number)
    # pprint.pprint(data)
    # res = requests.post("http://127.0.0.1:8080/ip/import_internet_ip_info/", data={"data": json.dumps(data)})

    # 导入内网网段，同步创建IP
    # excel = Excel("iplist.xlsx")
    # data = excel.load_sheet_content()
    # network_list = [i["子网地址"].split("/") for i in data]
    # res = requests.post("http://127.0.0.1:8080/ip/export_intranet_segment/", data={"data": json.dumps(network_list)})
    # print(res.ok)

    """
    network_list = [i["子网地址"].split("/") for i in data]
    print(f"实例化load数据： {data}")
    print(f"实例化load network列表： {network_list}")
    # bulk_list = []
    # for i in network_list:
    #     is_segment_in_db = IntranetSegment.objects.filter(netId=i[0])
    #     if not is_segment_in_db:
    #         intranet_seg_instance = IntranetSegment(netId=i[0], mask=i[1])
    #         bulk_list.append(intranet_seg_instance)
    #     IntranetSegment.objects.bulk_create(bulk_list)
    # print("db update success")

    ip_docs = xlrd.open_workbook("ip_docs.xlsx")
    print("文档表： ", len(ip_docs.sheets()))
    print(ip_docs.sheets()[0].name)
    print("*********************************************")

    ips = xlrd.open_workbook("iplist.xlsx")
    print("sheet数量： ", len(ips.sheet_names()))
    print("sheet obj: ", ips.sheets())
    sheet_name_list = [i.name for i in ips.sheets()]
    # for i in ips.sheets():
    #     print(i.name)
    #     print(dir(i))
    # print(ips.sheets()[0].ncols)
    # ncols = ips.sheets[0].ncols
    print(f'sheet名称列表： {sheet_name_list}')
    sheet = ips.sheet_by_name(sheet_name_list[1])
    print(sheet.name)
    print("0行2列： ", sheet.cell(0,2))

    print("name: ", sheet.name)
    print("ncols： ", sheet.ncols, "type: ", type(sheet.ncols))

    title, data = [], []
    for i in range(sheet.ncols):
        title.append(sheet.cell(0, i).value)

    for i in range(1, sheet.nrows):
        unit = {}
        for j in range(sheet.ncols):
            if sheet.cell(i, j).ctype == XL_CELL_NUMBER:
                unit[title[j]] = f'{sheet.cell(i, j).value}'
            else:
                unit[title[j]] = sheet.cell(i, j).value
        data.append(unit)

    print(f'read_file_title: {title}')
    pprint.pprint(data)
    """
