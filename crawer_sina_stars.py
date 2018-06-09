import requests
from bs4 import BeautifulSoup
import time
import json
import re
import urllib
import random





#写入TXT
def write_txt(data,filename):
    write_txt = open(filename, 'a+', encoding='utf-8')
    for i in data:
        if i:
             write_txt.write(str(i)+'\n')
    write_txt.close()


def get_ip(filename):
    ip_list = []
    with open(filename, 'r',encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            ip_list.append({'https':'http://'+str(line).strip('\n')})
    return ip_list

# def get_random_ip(filename):
#     with open(filename, 'r',encoding='utf-8') as f:
#         lines = f.readlines()
#         proxy_list = []
#         for ip in lines:
#             proxy_list.append('http://' + ip)
#             proxy_ip = random.choice(proxy_list)
#             proxies = {'http': proxy_ip}
#     return proxies



if __name__ == '__main__':

    #start_url = ''
    #第一页：http://ent.sina.com.cn/ku/star_search_index.d.html?page=1&cTime=1520118956&pre=pre
    #第二页：http://ent.sina.com.cn/ku/star_search_index.d.html?page=2&cTime=1520122188&pre=next
    #第三页：http://ent.sina.com.cn/ku/star_search_index.d.html?page=3&cTime=1519955355&pre=next
    #第四页：http://ent.sina.com.cn/ku/star_search_index.d.html?page=4&cTime=1519720432&pre=next

    # s = requests.Session()
    # s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'}

    #proxy_list = get_ip(r'G:\WorkSpace\python\Big_Crawer\IP_get\ip.txt')
    # proxy = random.choice(proxy_list)#随机选择一个代理
    # print(proxy)
    # 使用选择的代理构建代理处理器对象
    # httpproxy_handler = urllib.ProxyHandler(proxy)
    #
    # opener = urllib.build_opener(httpproxy_handler)
    #
    # request = urllib.Request("http://www.baidu.com/")
    # response = opener.open(request)
    # print
    # response.read()

    #next_page_url =
    start_url = 'http://ent.sina.com.cn/ku/star_search_index.d.html'
    for i in range(1,1968):
        try:
            #proxy = random.choice(proxy_list)  # 随机选择一个代理
            #print(proxy)
            print(start_url)
            name_list = []
            #html = s.get(start_url, proxies=proxy)
            html = requests.get(start_url,headers=headers)#proxies=proxy
            html.encoding = 'utf-8'
            soup = BeautifulSoup(html.text, 'lxml')

            stars_name = soup.find_all('h4',class_ = 'left')
            for i in stars_name:
                names = i.text.strip('\n')
                print(names)
                name_list.append(i.text.strip().strip('\n'))
            write_txt(name_list, r'sina_names.txt')
            start_url = soup.find('a',class_ = 'next-t nextPage')['href']
            random_time = random.randint(3,5)
            time.sleep(4+random_time)
        except TypeError:
            start_url = start_url
            time.sleep(600)

    #print(next_page_url)
        #print(next_page_url.links)

    #
    #write_txt(name_list,r'sina_names.txt')

    #s.close()
    print('OK')
