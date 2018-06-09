import requests
from bs4 import BeautifulSoup
import time
import json
import re
import urllib

#获取每个店铺链接地址
def getDetailInfo(url):
    product_id_list = []
    product_title_list = []
    name_id = []
    r = s.get(url)
    r.encoding = 'gb2313' #出现乱码后解决


    soup = BeautifulSoup(r.text, 'lxml')

    id_pattern = re.compile(r'data-pid="(.*?)"', re.S | re.M | re.I)

    title_list = soup.find_all('li', class_ = 'gl-item')
    #print(title_list)
    for i in title_list:
        title = i.find('div',class_ = 'p-name p-name-type-2').a.text.strip(' ').strip('\n')
        print(title)
        product_title_list.append(title)

        re_product_id = re.search(id_pattern, str(i))
        result = re_product_id.group(1)
        product_id_list.append(result)
    # for i,j in zip(product_title_list,product_id_list):
    #     name_id = '\t'.join([i,j])
    #     print(name_id)
    name_and_id = dict(zip(product_title_list,product_id_list ))

    return name_and_id

#进入每个页面，获取商品名与评论
def get_Name_comment(name_and_id_dic):
    comment_list = []
    for key,value in name_and_id_dic.items():
        #print(key,value)
        i = 1
        comment_count = 0
        while i<30:
            jd_comment_request = 'https://sclub.jd.com/comment/productPageComments.action?&productId='+ value+'&score=0&sortType=5&page='+str(i)+'&pageSize=10'
            #https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv190&productId=17974529774&score=0&sortType=5&page=1&pageSize=10&isShadowSku=0&rid=0&fold=1
            #https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv334&productId=13544621662&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1
            print(jd_comment_request)
            comment = s.get(jd_comment_request)
            #print(comment.text)
            #comment = '{'+ comment.text +'}'
            comment_json = json.loads(comment.text.strip(''))#
            #print(comment_json.keys())
            for each_comment in comment_json['comments']:
                #print(each_comment['rateContent'])
                #name_comment = [each_info[0],each_comment['rateContent']]
                a = each_comment['content'].replace('\n',' ')
                name_comment = '\t'.join([each_comment['referenceName'], a])
                print(name_comment)
                comment_list.append(name_comment)
                comment_count +=1
            i += 1

    return comment_list

if __name__ == '__main__':
    product = '荣耀v10'
    product = urllib.parse.quote(product) #编码为utf-8
    #print(product)
    deepth = 2 #第一页
    start_url = 'https://search.jd.com/Search?keyword=+'+product+'&enc=utf-8'  #
    #JD搜索url
    #https://search.jd.com/Search?keyword=%E9%9B%85%E8%BF%AA%E7%94%B5%E5%8A%A8%E8%BD%A6&enc=utf-8
    info_list = []
    detail_url_list = []
    news_content = []
    #comment_list = []
    comment_set = set()
    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
    write_txt = open("jd_荣耀v10_comment.txt", 'a+', encoding='utf-8')
    for i in range(1,deepth): #jd翻页的话需要设置步长为2，这里雅迪电动车只有一页故不设置
        url = start_url + '&page=' + str(i)
        name_and_id_dic = getDetailInfo(url) #这里只获取了产品ID，因为评论request中只需要id
        print('第%s页'%(i))

        name_and_comment = get_Name_comment(name_and_id_dic)
        for i in range(len(name_and_comment)):
            #print(name_and_comment[i])
            comment_set.add(name_and_comment[i])
        #print(len(comment_set))

        time.sleep(2)
    print(len(comment_set))
    for i in comment_set:
         write_txt.write(str(i)+'\n')
    write_txt.close()
    s.close()
    print('OK')
