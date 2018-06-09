#百度明星档案https://news.baidu.com/f/#a
#2018.5.7验证正常
import requests
from bs4 import BeautifulSoup

#写入TXT
def write_txt(data,filename):
    write_txt = open(filename, 'a+', encoding='utf-8')
    for i in data:
        if i:
             write_txt.write(str(i)+'\n')
    write_txt.close()



if __name__ == '__main__':
    name_list = []
    start_url = 'https://news.baidu.com/f/#b'

    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
    html = s.get(start_url)
    html.encoding = 'gbk' #出现乱码后解决
    soup = BeautifulSoup(html.text, 'lxml')
    #print(soup)
    stars_name = soup.find_all('td',class_ = 'ltd')
    for i in stars_name:
        name_list.append(i.text.strip().strip('\n'))
    write_txt(name_list,r'baidu_names.txt')

    s.close()
    print('OK')