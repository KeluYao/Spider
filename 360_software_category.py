#软件分类首页：http://zhushou.360.cn/list/index/cid/12/ 其中/12/为类型名； 思想：建立类型名-ID字典
#每个类型名共50页，翻页链接：
#第一页： http://zhushou.360.cn/list/index/cid/12/?page=1

import requests
from bs4 import BeautifulSoup
import time
import json
import re
import urllib

def get_catagoryName_id():
    #catagoryName = ['系统安全', '通讯社交', '影音视听', '新闻阅读', '生活休闲', '主题壁纸', '办公商务', '摄影商务','购物优惠','地图旅游','教育学习','金融理财','健康医疗']
    #catagoryId = ['11', '12', '14', '15', '16', '18', '17', '102228','102230','102231','102232','102139','102233']
    catagoryName = ['角色扮演', '休闲益智', '动作冒险', '网络游戏', '体育竞技', '飞行射击', '经营策略', '棋牌天地', '儿童游戏']
    catagoryId = ['101587', '19', '20', '100451', '51', '52', '53', '54', '102238']

    catagory_Name_Id = dict(zip(catagoryId,catagoryName))
    return catagory_Name_Id

def write_txt(result):
    write_txt = open("360_game_categoty.txt", 'a+', encoding='utf-8')
    for i in result:
         write_txt.write(str(i)+'\n')
    write_txt.close()



if __name__ == '__main__':
    catagory_Name_Id = get_catagoryName_id()

    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'

    for key, value in catagory_Name_Id.items():
        info_set = set()
        info_list = []
        for page in range(1,16):#51
            category_url = 'http://zhushou.360.cn/list/index/cid/'+str(key)+'/'+'?page='+str(page)
            print(category_url)
            category_html = s.get(category_url)
            soup = BeautifulSoup(category_html.text, 'lxml')
            category_info = soup.find('ul', class_ = 'iconList')


            #匹配<li>之间的内容失败
            # li_patern = re.compile(r'<li>(.*?)</li> ', re.S | re.M | re.I)
            # li_list = re.findall(li_patern,str(category_info))
            # print(li_list)
            li_list = []

            for each_software in category_info:
                #print(str(each_software))
                li_patern = re.compile(r'<li>(.*?)</a></li>', re.S | re.M | re.I)
                li_list.append(re.findall(li_patern,str(each_software)))

            #print(len(li_list))
            for each in li_list[1:50]:
                #print(str(each))
                try:
                    re_name = re.compile(r'name=(.*?)&amp', re.S | re.M | re.I)
                    re_download = re.compile(r'</a></h3><span>(.*?)</span>', re.S | re.M | re.I)
                    name = re.search(re_name,str(each))
                    download_count = re.search(re_download,str(each))
                    #print(name.group(1))
                    #print(download_count.group(1))

                    info = '\t'.join([value.strip('\n'), name.group(1).strip('\n'), download_count.group(1).strip('\n')])
                    print(info)
                    info_list.append(info)
                except AttributeError:
                    pass
        write_txt(info_list)

    s.close()
    print('OK')