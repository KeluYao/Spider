import requests
from bs4 import BeautifulSoup
import time
import json
import re

#获取每个店铺链接地址
def getDetailInfo(url):
    r = s.get(url)
    #print(r.text)
    #soup = BeautifulSoup(r.text, 'lxml')
    news_pattern = re.compile(r'{"pageName":"mainsrp",.*?false}}', re.S | re.M | re.I)
    web_content = re.search(news_pattern, r.text)
    #web_content = re.findall(news_pattern, r.text)
    result = web_content.group()  # 获得json格式
    #print(result)
    #print(result)
    #result = ''.join(web_content)
    pagejson = json.loads(result)  # 将str转换成dic

    for news in pagejson['mods']['itemlist']['data']['auctions']:  # 包含的信息在auctions内
        #print(news)
        #view_price = news['view_price']  # 价格
        #view_sales = news['view_sales']  # 销量
        #item_loc = news['item_loc']  # 所在地点

        raw_title = news['raw_title']  # 商品名
        nid = news['nid']  #店铺ID
        user_id = news['user_id']  #商家ID
        detail_url = news['detail_url'] #商品详情链接地址
        comment_url = news['comment_url'] #评论页链接地址
        #print(comment_url)
        comment_count = news['comment_count'] #评论总数

        is_tmall = news['shopcard']['isTmall']
        web_news = [raw_title, nid, user_id, detail_url, comment_url, comment_count, is_tmall]
        news_content.append(web_news)
        #detail_url_list.append(detail_url)
        #print(web_news)

    return news_content



#进入每个页面，获取商品名与评论
def get_Name_comment(detail_info):
    comment_list = []
    for each_info in detail_info[:]:
        i = 1
        if each_info[6] == True:
            print('istmall')
            comment_count = 0
#存在两个问题，1.评论总数造假，少于实际评论数，2.后几百页评论相同
            #print('istmall')
            while i<20:
                try:
                    tmall_comment_request = 'https://rate.tmall.com/list_detail_rate.htm?itemId='+str(each_info[1])+'&sellerId='+str(each_info[2])+'&order=3&currentPage='+str(i)
                    print(tmall_comment_request)
                    comment = s.get(tmall_comment_request)
                    #print(comment.text)
                    comment = '{'+ comment.text +'}'
                    comment_json = json.loads(comment.strip(''))#
                    for each_comment in comment_json['rateDetail']['rateList']:
                        #print(each_comment['rateContent'])
                        #name_comment = [each_info[0],each_comment['rateContent']]
                        name_comment = '\t'.join([each_info[0], each_comment['rateContent']])
                        print(name_comment)
                        comment_list.append(name_comment)
                        #print(comment_list)
                        comment_count +=1
                    i += 1
                    #time.sleep(2)
                except:
                    i = i
                #print('评论页数:'+str(i)+'评论总数'+str(int(each_info[5]))+'已爬取评论数:'+str(comment_count))
        else:
            print('淘宝店铺跳过')
            #time.sleep(1)
            #淘宝店铺获取的json暂时有问题，暂未修改，故pass
            # comment_count = 0
            # i = 1
            # #print('istmall')
            # while i<150:
            #     taobao_comment_request = 'https://rate.taobao.com/feedRateList.htm?auctionNumId=' + str(each_info[1]) + '&userNumId=' + str(each_info[2]) + '&currentPageNum=' + str(i)
            #     comment = s.get(taobao_comment_request)
            #     comment = '{'+comment.text +'}'
            #     comment_json = json.loads(comment.strip(''))#
            #     for each_comment in comment_json['rateDetail']['rateList']:
            #         #print(each_comment['rateContent'])
            #         #comment_list.append(each_comment['rateContent'])
            #         name_comment = [each_info[0],each_comment['rateContent']]
            #         comment_list.append(name_comment)
            #         comment_count +=1
            #     i += 1
            #     print('评论页数:'+str(i)+'评论总数'+str(int(each_info[5]))+'已爬取评论数:'+str(comment_count))
            # #i = 1
            # #taobao_comment_request = 'https://rate.taobao.com/feedRateList.htm?auctionNumId='+str(each_info[1])+'&userNumId='+str(each_info[2])+'&currentPageNum='+str(i)
            # #print(taobao_comment_request)
    #print(comment_list)
    return comment_list

if __name__ == '__main__':
    product = '荣耀v10'
    deepth = 1
    start_url = 'https://s.taobao.com/search?q=' + product + '&sort=sale-desc&fs=1&filter_tianmao=tmall'  #后面一部分字符串为按销量从高到低，只看天猫
    #https://s.taobao.com/search?q=佳能打印机&bcoffset=0&ntoffset=0&s=0
    #link = r'https://s.taobao.com/search?q=%E4%BD%B3%E8%83%BD+%E6%89%93%E5%8D%B0%E6%9C%BA&imgfile=&js=1&stats_click=search_radio_tmall%3A1&initiative_id=staobaoz_20180224&tab=mall&ie=utf8%E2%80%99'
    #只选天猫
    #https://s.taobao.com/search?initiative_id=tbindexz_20170306&ie=utf8&spm=a21bo.2017.201856-taobao-item.2&sourceId=tb.index&search_type=item&ssid=s5-e&commend=all&imgfile=&q=%E8%8E%B1%E5%85%8B%E5%87%80%E5%8C%96%E5%99%A8&suggest=history_2&_input_charset=utf-8&wq=&suggest_query=&source=suggest&sort=sale-desc&fs=1&filter_tianmao=tmall
    info_list = []
    detail_url_list = []
    news_content = []
    #comment_list = []
    comment_set = set()
    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
    write_txt = open("taobao_荣耀v10_comment.txt", 'a+', encoding='utf-8')
    for i in range(deepth):
        url = start_url + '&s=' + str(44 * i)
        detailInfo = getDetailInfo(url)
        print('第%s页'%(i+1))
        #detailInfo2 = change_detail_info(detailInfo)
        #print('第二部分执行完')
        name_and_comment = get_Name_comment(detailInfo)
        for i in range(len(name_and_comment)):
            comment_set.add(name_and_comment[i])
        #print(len(comment_set))


        time.sleep(2)
    print(len(comment_set))
    for i in comment_set:
        write_txt.write(str(i)+'\n')
    write_txt.close()
    s.close()
    print('OK')
