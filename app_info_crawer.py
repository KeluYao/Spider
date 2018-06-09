#需求：分类名：catagory，APP名：app_name，下载次数：appDownCount,MD5：apkMd5,下载地址：apkUrl, 软件介绍：editorinto
#下拉的请求
#购物
#原始页 http://sj.qq.com/myapp/category.htm?orgame=1&categoryId=122
#第一页：http://sj.qq.com/myapp/cate/appList.htm?orgame=1&categoryId=122&pageSize=20&pageContext=87
#第二页：http://sj.qq.com/myapp/cate/appList.htm?orgame=1&categoryId=122&pageSize=20&pageContext=108

#阅读
#原始页 http://sj.qq.com/myapp/category.htm?orgame=1&categoryId=122
#第一页： http://sj.qq.com/myapp/cate/appList.htm?orgame=1&categoryId=102&pageSize=20&pageContext=80
#第二页：

#通讯
#原始页：http://sj.qq.com/myapp/category.htm?orgame=1&categoryId=116
#第一页：http://sj.qq.com/myapp/cate/appList.htm?orgame=1&categoryId=116&pageSize=20&pageContext=67
#第二页：http://sj.qq.com/myapp/cate/appList.htm?orgame=1&categoryId=116&pageSize=20&pageContext=102

#点分类的请求
#购物 http://sj.qq.com/myapp/category.htm?orgame=1&categoryId=122
#阅读 http://sj.qq.com/myapp/category.htm?orgame=1&categoryId=102
#安全 http://sj.qq.com/myapp/category.htm?orgame=1&categoryId=118
#思想：url+id，id为固定值，无规律，建立字典

#游戏页面下拉的请求
#第一页：http://sj.qq.com/myapp/cate/appList.htm?orgame=2&categoryId=146&pageSize=20&pageContext=54
#第二页：http://sj.qq.com/myapp/cate/appList.htm?orgame=2&categoryId=146&pageSize=20&pageContext=77
#第三页：http://sj.qq.com/myapp/cate/appList.htm?orgame=2&categoryId=146&pageSize=20&pageContext=106

import requests
from bs4 import BeautifulSoup
import time
import json
import re
import urllib

def get_catagoryName_id():
    #catagoryName = ['购物','阅读','新闻','视频','旅游','工具','社交','音乐','美化','摄影','理财','系统','生活','出行','安全','教育','健康','娱乐','儿童','办公','通讯']
    #catagoryId = ['122','102','110','103','108','115','106','101','109','104','114','117','107','112','118','111','109','105','100','113','116']
    catagoryName = ['休闲益智', '网络游戏', '飞行射击', '动作冒险', '体育竞速', '棋牌中心', '经营策略', '角色扮演']#修改为体育竞速，未跑数据
    catagoryId = ['147', '121', '149', '144', '151', '148', '153', '146',]
    catagory_Name_Id = dict(zip(catagoryId,catagoryName))
    return catagory_Name_Id

def write_txt(result):
    write_txt = open("yingyongbao_youxi.txt", 'a+', encoding='utf-8')
    for i in result:
         write_txt.write(str(i)+'\n')
    write_txt.close()




if __name__ == '__main__':
    catagory_Name_Id = get_catagoryName_id()
    #info_set = set()
    info_dic = {}
    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
    #r0 = s.get('http://sj.qq.com/myapp/cate/appList.htm?orgame=1&categoryId=116&pageSize=20&pageContext=0')
    # r3 = s.get('http://sj.qq.com/myapp/cate/appList.htm?orgame=1&categoryId=116&pageSize=20&pageContext=1')
    #r1=s.get('http://sj.qq.com/myapp/cate/appList.htm?orgame=1&categoryId=116&pageSize=20&pageContext=67')
    #r2 = s.get('http://sj.qq.com/myapp/cate/appList.htm?orgame=1&categoryId=116&pageSize=20&pageContext=107')

    # print(r0.text)
    # print(r3.text)
    #print(r1.text)
    # print(r2.text)
    #r1_json = json.loads(r1.text.strip(''))  #
    # for i in r1_json['obj']:
    #     print(i['appName'])
    #     print(i['appDownCount'])
    #     print(i['apkMd5'])
    #     print(i['apkUrl'])
    #     print(i['editorIntro'])


    for key, value in catagory_Name_Id.items():
        info_set = set()
        for j in range(0,121,20):
            #try:
            print(j)
            #start_url = 'http://sj.qq.com/myapp/cate/appList.htm?orgame=1&categoryId='+str(key)+'&pageSize=20&pageContext='+str(j)
            start_url = 'http://sj.qq.com/myapp/cate/appList.htm?orgame=2&categoryId='+str(key)+'&pageSize=20&pageContext='+str(j)
            print(start_url)
            r = s.get(start_url, timeout = 20)
            time.sleep(1)
            r1_json = json.loads(r.text.strip(''))  #
            for i in r1_json['obj']:
                categoryId = i['categoryId']
                appId = i['appId']
                print(appId)
                catagoryName = value
                appName = i['appName']
                appDownCount= i['appDownCount']
                apkMd5 = i['apkMd5']
                apkUrl = i['apkUrl']
                editorIntro = i['editorIntro']
                #info = [catagoryName, appName, appDownCount, apkMd5, apkUrl, editorIntro]
                info2 = '\t'.join([str(categoryId),catagoryName,appName,apkMd5,apkUrl,editorIntro,str(appId)])
                #print(type(info2))

                #print(info)
                print(info2)

                info_set.add(info2)
            # except:
            #     print('页面未获取')
        write_txt(info_set)
        print(len(info_set))
    # for i in info_set:
    #     write_txt(i)

    s.close()
    print('OK')