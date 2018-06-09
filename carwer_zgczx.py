#中关村在线根据手机型号爬取对应帖子内容
import time

import re
from bs4 import BeautifulSoup as BS

from selenium import webdriver

import selenium.webdriver.support.ui as ui

import requests

driver = webdriver.Firefox()
wait = ui.WebDriverWait(driver, 10)
driver.get(r'http://detail.zol.com.cn/1168/1167243/review.shtml')
list1 =[]
try:
    while 1:
        driver.find_element_by_id('_j_view_more_comments').click()
except:
    print('到头了')
    time.sleep(90)
    pass
# for i in range(18):
#     driver.find_element_by_id('_j_view_more_comments').click()

content_list = driver.find_elements_by_class_name('comments-item')
for each_content in content_list:
    title = each_content.find_element_by_class_name('title').text.replace('\n',':')
    score = each_content.find_element_by_class_name('single-score')
    star = score.text.split('\n')[0]
    star = '总评分'+':'+str(star)
    single_star_list = score.find_elements_by_tag_name('p')
    single_star = ''
    for each_score in single_star_list:
        single_star= single_star + each_score.text
    content = each_content.find_elements_by_class_name('words')
    good_and_bad = ''
    for i in content:
        a = i.text.replace('\n','')
        good_and_bad = good_and_bad + a
    list1.append('|'.join([title,star,single_star,good_and_bad]))

with open(r'荣耀9_中关村在线.txt','w+',encoding='utf-8') as f:
    for i in list1:
        f.write(i+'\n')


