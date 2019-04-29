import requests
from lxml import etree

file = open('all2.txt','w+',encoding='utf-8')
headers = {
            'Host': 'med.39.net',
            'Connection': 'keep-alive',
            # 'Cache-Control': 'max-age=0',
            # 'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': 'ASP.NET_SessionId=tv5bqwr40psnvk45bmzfvsbk; Hm_lvt_eeeef2d289cfb1ec7eb1a2771c02a426=1554197582,1554796100; Hm_lpvt_eeeef2d289cfb1ec7eb1a2771c02a426=1554796100',
            'If-Modified-Since': 'Tue, 09 Apr 2019 07:48:17 GMT',
}

url_prefix = 'http://med.39.net/cds/ywxhzy/list2-'
url_postfix = '.shtml'
now_num = 392
for cate_i in range(17,23):
    session = requests.session()
    start_url = f'{url_prefix}{cate_i}-{cate_i}-{now_num}-1{url_postfix}'
    response = session.get(url=start_url,headers=headers)
    #//*[@id="form1"]/div[6]/p/i
    root = etree.HTML(response.text)
    num = root.xpath('//*[@id="form1"]/div[6]/p/i/text()')[0]

    #计算多少页
    pages_multi = int(int(num)/10)
    pages_remain = int(int(num)%10)
    if pages_remain:
        pages = pages_multi+1
    else:
        pages = pages_multi

    #先首页写入文件
    items = root.xpath('string(//*[@id="form1"]/div[6]/ul)')
    file.write(items)

    for page in range(pages-1):
        cur_url = f'{url_prefix}{cate_i}-{cate_i}-{now_num}-{page+2}{url_postfix}'
        cur_response = session.get(url=cur_url,headers=headers)
        cur_root = etree.HTML(cur_response.text)
        items = cur_root.xpath('string(//*[@id="form1"]/div[6]/ul)')
        file.write(items)
    now_num+=1
    print(cate_i)