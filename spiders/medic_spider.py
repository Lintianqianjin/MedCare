import json
import re
import requests
from bs4 import BeautifulSoup

import io
import sys
from selenium import webdriver

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')  # 改变标准输出的默认编码

file1 = open("medic1.json", "w", encoding="utf-8")
flag = False


def getHTMLText(_url):
    try:
        r = requests.get(_url, timeout=30)
        r.raise_for_status()
        # r.encoding = r.apparent_encoding # 这里apparent_encoding 识别不准！
        r.encoding = "utf-8"
        return r.text
    except:
        return ""


def get_urls(main_url):
    global flag
    content = getHTMLText(main_url)
    soup = BeautifulSoup(content, 'lxml')
    fns = soup.findAll('div', attrs={"class": "fn"})
    urls = []
    datas = []
    for fn in fns:
        # print(fn)
        urls.append(fn.a['href'])
    print(urls)
    for u in urls:
        try:
            data = get_infos(u)
            if flag:
                datas.append(data)
            else:
                pass
        except:
            pass

    json.dump(datas, file1, ensure_ascii=False)
    return urls, datas


def get_infos(sub_url):
    global flag
    content = getHTMLText(sub_url)

    # print(content)

    reg0 = re.compile(r'page__title\'>(.*?)</h1')
    reg1 = re.compile(r'<th>相关症状</th>\n<td>(.*?)</td>')
    reg2 = re.compile(r'\'details\'>\n<a target="_blank" href="(.*?)">')
    reg3 = re.compile(r'\'details\'>\n<a target="_blank" href=".*?">(.*?)</a')

    name = re.findall(reg0, content)[0]

    if name == '食物过敏性哮喘':
        flag = True

    if not flag:
        return

    zhengzhuang = re.findall(reg1, content)
    yaowu_names = re.findall(reg3, content)
    yaowu_urls = re.findall(reg2, content)

    dict = {}

    dict['name'] = name
    if zhengzhuang.__len__() > 0:
        dict['zhengzhuang'] = zhengzhuang[0].split(';')
    else:
        zhengzhuang = ""
    yaowu = []
    for i in range(yaowu_names.__len__()):
        yaowu.append({'yw_name': yaowu_names[i], 'nos': get_medics(yaowu_urls[i])})
    dict['yaowu'] = yaowu
    print(dict)
    # file2.write(dict + '\n')

    file2 = open("medic1.txt", "a", encoding="utf-8")
    file2.write(str(dict) + '\n')
    # file2.write('111')
    file2.close()
    return dict


def get_medics(medic_url):
    content = getHTMLText(medic_url)
    # print(content)

    reg1 = re.compile(r'国药准字([a-zA-Z][0-9].*?)</a>')
    yaowus = re.findall(reg1, content)
    # print(yaowus)

    return yaowus


if __name__ == '__main__':
    get_urls('https://www.yaozui.com/jibing')
    # get_infos('https://www.yaozui.com/jibing/4338-aizibing')
    # get_medics('https://www.yaozui.com/yaopin/1034-yansuanduoroubixingzhizhitizhusheye')
    # print(getHTMLText('https://www.baidu.com/s?ie=UTF-8&wd=hhhh'))
