import requests
from bs4 import BeautifulSoup
import time
import re
s = requests.Session()
s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'

all_list = []
for i in range(1,197):
    start_url = 'http://zq.games.sina.com.cn/ol/?zx=1&p='+ str(i)
    html = s.get(start_url)
    html.encoding = 'utf-8'  # 出现乱码后解决
    soup = BeautifulSoup(html.text, 'lxml')
    content_list = soup.find_all('div',class_ = 'sec_con')

    for each in content_list:
        res = []
        a = each.find('h2').a.text
        res.append(a)
        b = each.find('div',class_ = 'sec_style')
        c_list = b.find_all('span')
        for i in c_list:
            res.append(i.text)
        each_one = '\t'.join(res)
        print(each_one)
        all_list.append(each_one)
    time.sleep(1)

with open('1.txt','w+',encoding='utf-8') as f:
    for i in all_list:
        f.write(i+'\n')

