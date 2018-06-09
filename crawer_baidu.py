#百度贴吧标题获取



import requests
import re
import time
#下面三行是编码转换的功能，大家现在不用关心。

# html = requests.get('http://tieba.baidu.com/f?kw=华为&ie=utf-8&pn=250')
# print(html.text)
# html.encoding = 'utf-8' #将编码转为utf-8FA防止中文乱码。
#
# title = re.findall('class="j_th_tit ">(.*?)</a>',html.text,re.S)
#
# for TITLE in title:
#     print(TITLE)

list1 = []
s = requests.session()
s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'

for i in range(0,2200,50):
    print(i)
    url = 'http://tieba.baidu.com/f?kw=荣耀&ie=utf-8&pn='
    url = url +str(i)
    print(url)
    r = s.get(url)
    print(r.status_code)
    title = re.findall('class="j_th_tit ">(.*?)</a>',r.text,re.S)
    for j in title:
        j = re.sub('<span class="topic-tag" data-name="(.*?)">','',str(j)).replace('</span>','')
        print(j)
        list1.append(j)
    time.sleep(4)

with open(r'贴吧_荣耀.txt','a+',encoding='utf-8') as f:
    for each in list1:
        f.write(each+'\n')



# content_list = soup.find_all('div',class_ = r'wrap1t')
# print(content_list)
# for each_content in content_list:
#     a = each_content.find('div',class_ = 'j_th_tit ').get('title')
#     print(a)
# s.close()
