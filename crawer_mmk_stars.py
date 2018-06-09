import requests
import re
from bs4 import BeautifulSoup

def write_txt(data,filename):
    write_txt = open(filename, 'a+', encoding='utf-8')
    for i in data:
        if i:
             write_txt.write(str(i)+'\n')
    write_txt.close()

def get_name(url):
    name_list = []
    pattern = re.compile(r'title="(.*?)"',re.S | re.M | re.I)
    html = s.get(url, timeout=10)
    html.encoding = 'gbk'
    soup = BeautifulSoup(html.text, 'lxml')
    name_info = soup.find_all('div', class_='i_cont_s')
    for each in name_info:
        names = re.findall(pattern, str(each))
        for i in names:
            name_list.append(i)
    return name_list


if __name__ == '__main__':

    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'

    geshou_url = 'http://www.manmankan.com/dy2013/mingxing/geshou/'
    yanyuan_url = 'http://www.manmankan.com/dy2013/mingxing/yanyuan/'
    geshou_list = get_name(geshou_url)
    yanyuyan_list = get_name(yanyuan_url)

    write_txt(geshou_list,r'mmk_stars.txt')
    write_txt(yanyuyan_list,r'mmk_stars.txt')


