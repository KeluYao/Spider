#2018.5.7验证正常
import requests
import re
from bs4 import BeautifulSoup
import time

def write_txt(data,filename= r'mmk2_stars.txt'):
    write_txt = open(filename, 'a+', encoding='utf-8')
    for i in data:
        if i:
             write_txt.write(str(i)+'\n')
    write_txt.close()

def get_name(url):
    name_list = []
    pattern = re.compile(r'title="(.*?)"',re.S | re.M | re.I)
    html = s.get(url, timeout=20)
    html.encoding = 'gbk'
    soup = BeautifulSoup(html.text, 'lxml')
    name_info = soup.find('div', class_='i_cont')
    names = re.findall(pattern, str(name_info))
    for i in names:
        print(i)
        name_list.append(i)
    return name_list


if __name__ == '__main__':
    name_list = ['start']
    s = requests.Session()
    #s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
    s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
    s.headers['Host'] = 'www.manmankan.com'

    A_Z = [chr(x).upper() for x in range(97, 123)]
    for each in A_Z:
        start_url = 'http://www.manmankan.com/dy2013/mingxing/'+ each +'/'#修改第一页中的AB...

        name_1 = get_name(start_url)
        write_txt(name_1)
    #
        for i in range(2,20):#修改页数
            try:
                next_url =start_url+'index_'+str(i)+'.shtml'#修改A
                name_list = get_name(next_url)
                write_txt(name_list)
                time.sleep(1)
            except:
                break



