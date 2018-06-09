#2018.5.7验证正常

import requests
import re

def write_txt(data,filename):
    write_txt = open(filename, 'a+', encoding='utf-8')
    for i in data:
        if i:
             write_txt.write(str(i)+'\n')
    write_txt.close()


s = requests.Session()
s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'

name_list = []
pattern = re.compile(r'<h2>(.*?)</h2>',re.S | re.M | re.I)
for i in range(1,154): #最大153页
    url = 'http://www.ylq.com/star/list-all-all-all-all-all-all-all-'+str(i)+'.html'
    html = s.get(url)

    names = re.findall(pattern,str(html.text))
    print(names)
    for i in names:
        name_list.append(i)
write_txt(name_list,r'ylq.txt')


