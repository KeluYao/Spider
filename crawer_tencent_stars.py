#2018.5.7验证正常
import requests
from bs4 import BeautifulSoup
import re

#写入TXT
def write_txt(data,filename):
    write_txt = open(filename, 'a+', encoding='utf-8')
    for i in data:
        if i:
             write_txt.write(str(i)+'\n')
    write_txt.close()

if __name__ == '__main__':
    start_url = 'http://ent.qq.com/c/all_star.shtml'

    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
    html = s.get(start_url)
    html.encoding = 'gbk' #出现乱码后解决
    soup = BeautifulSoup(html.text, 'lxml')
    #print(soup)
    a = soup.find('div',class_ = 'index_cot_list')
    name_pattern = re.compile(r'title="(.*?)"', re.S | re.M | re.I)
    name_list = re.findall(name_pattern, str(a))
    for i in name_list:
        print(i)
    write_txt(name_list,r'tencent_names.txt')

    s.close()
    print('OK')