# -*- coding:utf-8 -*-
import urllib.request
import re
from urllib.request import quote, unquote
import json


medicine_instruction_list = []


# 获取网页html文档


def get_content(name):
    url_original = 'http://www.360haoyao.com/search?q=' + name + '&from_type=searchButton'
    url = quote(url_original, safe=";/?:@&=+$,", encoding="utf-8")  # 中文解码
    response = urllib.request.urlopen(url)  # 打开网址
    html = response.read().decode('utf-8')  # 读取源代码并转为unicode
    return html


# 获得药品详细信息


def get_url(html):
    reg = re.compile(r'<div class="seListBox">.*?<ul class="seachListBox">.*? <a href="(.*?)"  pt_pos_lid=',
                     re.S)  # 匹配换行符
    items = re.findall(reg, html)
    return items


# 获得药品说明书


def get(item):
    url = item[0]
    response = urllib.request.urlopen(url)

    html = response.read().decode('gbk')
    # 缩小范围
    reg_original = re.compile(r'<!--说明书start-->(.*?)<!--说明书end-->', re.S)
    detail = re.findall(reg_original, html)
    # 获得说明书信息
    reg = re.compile(r'<tr><th>(.*?)</th><td>(.*?)</td></tr>', re.S)
    items = re.findall(reg, detail[0])

    return items


# 读取药物名称

#打开json文件提取药品名称
with open("medic.json", "r", encoding="utf-8") as f:
    json_str = f.read()
medicine_list = json.loads(json_str)


name_list = []            # 原始药品列表
name_list_no_repeat = []   # 去重药品列表


for s in range(len(medicine_list)):
    if (medicine_list[s]['yaowu']):
        for k in range(len(medicine_list[s]['yaowu'])):
            name_list.append(medicine_list[s]['yaowu'][k]['yw_name'])

for s in  range(len(name_list)):
    if(not name_list[s] in name_list_no_repeat):
        name_list_no_repeat.append(name_list[s])

print(name_list_no_repeat)
print(len(name_list_no_repeat))

for s in range(len(name_list)):
    try:
        items = dict(get(get_url(get_content(name_list_no_repeat[s]))))
        items_format = {}
        items_format['通用名称'] = items.get('通用名称：')
        items_format['商品名称'] = items.get('商品名称：')
        items_format['成份'] = items.get('成份：')
        items_format['主治功能'] = items.get('功能主治：')
        items_format['用法用量'] = items.get('用法用量：')
        items_format['注意事项'] = items.get('注意事项：')
        items_format['不良反应'] = items.get('不良反应：')
        items_format['禁忌'] = items.get('禁忌：')
        items_format['药物相互作用'] = items.get('药物相互作用：')
        items_format['药理毒理'] = items.get('药理毒理：')
        items_format['药代动力学'] = items.get('药代动力学：')
        items_format['有效期'] = items.get('有效期：')
        items_format['妊娠期妇女及哺乳期妇女用药'] = items.get('妊娠期妇女及哺乳期妇女用药：')
        items_format['儿童用药'] = items.get('儿童用药：')
        items_format['老年患者用药'] = items.get('老年患者用药：')
        items_format['企业名称'] = items.get('企业名称：')
        items_format['适应症'] = items.get('适应症：')
        print(items_format)
        #        if('性状' in items.keys()):
        medicine_instruction_list.append(items_format)
    except:
        pass

with open("medicine_instruction_list_new.json", "w", encoding='utf-8') as f:
    json.dump(medicine_instruction_list, f, ensure_ascii=False)

f.close()
