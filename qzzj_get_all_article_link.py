from bs4 import BeautifulSoup
import requests
import time

#写入函数
def write_txt(result_list,filename):
    write_txt = open(filename, 'w+', encoding='utf-8')
    for i in result_list:
         write_txt.write(str(i)+'\n')
    write_txt.close()

#获取口碑页中所有精华帖详细页面的链接，对应页面中“查看全部内容”
def get_all_article_link(url):

    r = s.get(url)
    if r.status_code == 200:
        print('访问成功')
    else:
        print('访问失败{}'.format(url))
    soup = BeautifulSoup(r.text, 'lxml')
    div_link = soup.find_all('div',class_ = 'allcont border-b-solid')
    print(div_link)
    for i in div_link:
        link = 'http:'+str(i).split('"')[5]   #根据”切分字符串，发现[5]是url地址，获取并存储到list中
        print(link)
        all_article_link.append(link)


    #return all_article_link

if __name__ == '__main__':
    s = requests.session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'

    all_article_link = []
    url_1 = 'https://k.autohome.com.cn/812/?pvareaid=2099118'
    get_all_article_link(url_1)
    time.sleep(10)

    for i in range(2,10):#共9页
        url = 'https://k.autohome.com.cn/812/index_'+str(i)+'.html?pvareaid=2099118#dataList'
        get_all_article_link(url)
        time.sleep(10)
    #write_txt(all_article_link,'Q5_all_article_link.txt')
    s.close()