import re

import requests
import time
import random

headers = {
            'Host': 'www.go007.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9'
}

url_head = "http://www.go007.com/ditu/zhenzhuang/p"

def getHTMLText(url_complete):
    try:
        r = requests.get(url_complete, timeout=30,headers=headers)
        r.raise_for_status()
        # r.encoding = r.apparent_encoding # 这里apparent_encoding 识别不准！
        r.encoding = "utf-8"
        return r.text
    except:
        print(r.status_code)
        print("爬取失败")
        return "爬取失败"

def get_fulltext(url_head):
    reg_head = re.compile(r'<i></i>(.*?)</a></h3>')
    reg_body = re.compile(r'<a href=.*?>(.*?)</a>')
    dict={}
    num = 1
    while (num <= 20):
        content = getHTMLText(url_head + str(num))
        print(num)
        time.sleep(random.random() * 3)
        num+=1
        name = re.findall(reg_head, content)
        for i in range(name.__len__()):
            body = []
            reg_body_full = re.compile(name[i] + r'</a></h3>.*?' + '<p>(.*?)</p>' + '.*?</li>')
            body_full = re.findall(reg_body_full, content)
            for s in range(body_full.__len__()):
                body = re.findall(reg_body, body_full[s])
                dict[name[i]] = body
                for y in range(body.__len__()):
                    print(name[i] + "  " + body[y])
    with open('medicine_1_2.txt', 'w') as f:
        for i in dict:
            f.write(i)

if __name__ == '__main__':
    get_fulltext(url_head)

