import requests
from selenium import  webdriver
import time
import urllib
import selenium.webdriver.support.ui as ui
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
import random

def write_txt(data,filename):
    write_txt = open(filename, 'a+', encoding='utf-8')
    for i in data:
        if i:
             write_txt.write(str(i)+'\n')
    write_txt.close()


if __name__ == '__main__':


    driver = webdriver.Firefox()

    driver.get(r'http://ent.sina.com.cn/ku/star_search_index.d.html')
    for i in range(1,1968):
        print('第%s页'%str(i))
        name_list = []
        #names_list = driver.find_elements_by_css_selector('div.item-title clearfix')
        names_list_2 = driver.find_elements_by_css_selector('h4.left')
        #print(names_list_2.text)

        for j in range(len(names_list_2)):
            name = names_list_2[j].text
            print(name)
            name_list.append(name)

        write_txt(name_list,r'sina_names.txt')

        driver.find_element_by_css_selector('.next-t').click()
        num = random.randint(4,8)
        time.sleep(num)

    driver.quit()
    write_txt.close()
    print('OK')