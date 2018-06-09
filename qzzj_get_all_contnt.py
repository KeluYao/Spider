from bs4 import BeautifulSoup
import re
import string
import urllib
import requests
import traceback
from collections import defaultdict
from fontTools.ttLib import TTFont
import urllib.request
from lxml import html
import time

#写入函数
def write_txt(result_list,filename):
    write_txt = open(filename, 'a+', encoding='utf-8')
    write_txt.write(result_list + '\n' )
    write_txt.close()

#从txt中得到link
def get_link(link_path):
    link_list = []
    with open(link_path,'r',encoding='utf-8') as f:
        for link in f:
            link_list.append(link.strip('\n'))
    return link_list

#获取到一个link中所有需要的内容，return content（...\t...\t...）, list_title_con_js（[...|...|...|, ...|...|...|, ...]）
def get_content(link):

    r = requests.get(link,headers=headers)
    if r.status_code != 200:
        print('访问失败')
    soup = BeautifulSoup(r.text, 'lxml')
    font_content = soup.find('div', class_ = 'content')  ##这里报错，说明遇到了反扒，页面中需要验证，查看浏览器中页面或者多执行几次
    # 匹配ttf font 地址
    #字体文件为打开页面时生成，故获取连接地址，下载
    #url('//k2.autoimg.cn/g17/M0A/F0/C7/wKgH51oXuvWAEsRYAADO8C6H2HY19..ttf') format('woff');
    #解决方案1：先用正则匹配出所在<style>区域，再匹配出tff文件地址
    url_in_style_pattern = re.compile(r'<style>(.*?)</style>', re.S | re.M | re.I)
    url_in_style = re.findall(url_in_style_pattern, str(font_content))
    font_url_pattern = re.compile(r"url\(.*?\)", re.S | re.M | re.I)
    font_url = re.findall(font_url_pattern, str(url_in_style))
    font_url_final ='http:' + font_url[2].strip('url(\'').strip('\\').strip('\')').strip("\\") #生成的字体文件下载地址
    #ttf = requests.get(font_url_final,headers = headers, stream=True)
    # with open("font_file", "wb") as f:
    #     f.write(ttf.content)
    urllib.request.urlretrieve(font_url_final,r'font_file2')  #获取连接地址中的文件，requests方式实测不可行

    choose_con = soup.find('div',class_ = 'choose-con')
    choose_d1 = choose_con.find_all('dl',class_ = 'choose-dl')#这里报错，说明遇到了反扒，页面中需要验证，查看浏览器中页面或者多执行几次
    #获取左边结构化部分
    content = ''
    for d1 in choose_d1:
        dt = d1.dt.text.strip()
        dd = d1.dd.text.replace('\n',' ').replace('\xa0','').strip()
        dt_dd = dt+':'+dd

        content = '\t'.join([content,dt_dd]).strip()
    #获取右边所有文字
    text_con = soup.find_all('div',class_='text-con')[-1]
    list_title_con_js = []
    a = []
    part_con_list = str(text_con).split('【')[1:]
    """获取标题与内容和混淆的js代码"""
    # 获取小标题
    for part_con in part_con_list:
        title = part_con.split("】")[0]
        # 获取加密的文本
        start = re.search('<!--@athm_BASE64@-->', part_con).span()[1]
        end = re.search('<!--@athm_js@-->', part_con).span()[0]
        part_base64 = part_con[start: end]#.replace('\n',' ')
        # 获取混淆的js代码
        soup_part = BeautifulSoup(part_con, "lxml")
        # print(soup_part)
        h_js = soup_part.find('script')#.replace('\n',' ')
        # 将标题和混淆的js存入一个列表
        test = '|'.join([str(title), str(part_base64).replace('\n',' '), str(h_js)])
        #print(test)
        #test = [str(title), str(part_base64), str(h_js)]
        #a.append(test)
        list_title_con_js.append(test)
    #print(len(list_title_con_js),list_title_con_js)
    return content, list_title_con_js

#定义替换函数
def change(str,rule_index,x):
    str_new = ''
    str_change = []
    str_split = str.split(x)
    #print(len(str_split),str_split)
    for i in str_split:
        if i in rule_dict_list[rule_index]:
            #print(i)
            str_change.append(rule_dict_list[rule_index][i])
        else:
            pass
            #print(i)
    for i in str_change:

        i = i.strip('\'').strip('\'')
        #print(i)
        str_new += i
    #print(str_new)
    return str_new


#解析字体库，得到编码与字的对应关系
def get_code_word_relation():
    # 解析字体库，得到编码与字体的对于关系
    font = TTFont(r'G:\WorkSpace\python\Big_Crawer\crawer_qczj2\font_file2')
    uniList = font['cmap'].tables[0].ttFont.getGlyphOrder()
    codeList = []
    for i in uniList[1:]:
        codeList.append(i.strip('uni').lower())
    #这些字是前端人工定义好的，是不变的，变的是编码；
    wordList = ['一', '七', '三', '上', '下', '不', '中', '档', '比', '油', '泥', '灯',
                '九', '了', '二', '五', '低', '保', '光', '八', '公', '六', '养', '内', '冷',
                '副', '加', '动', '十', '电', '的', '皮', '盘', '真', '着', '路', '身', '软',
                '过', '近', '远', '里', '量', '长', '门', '问', '只', '右', '启', '呢', '味',
                '和', '响', '四', '地', '坏', '坐', '外', '多', '大', '好', '孩', '实', '小',
                '少', '短', '矮', '硬', '空', '级', '耗', '雨', '音', '高', '左', '开', '当',
                '很', '得', '性', '自', '手', '排', '控', '无', '是', '更', '有', '机', '来']
    code_word_relation = dict(zip(codeList, wordList))
    return code_word_relation

#根据每个Link得到的内容，替换其中被替换文本
def get_replaced_content(content, list_title_con_js,code_word_relation):
    rule_dict = {} #保存变量的替换规则
    index_word_relation = {} #文字编码与原文中下标的对应关系（原文中相同文字只算一次）
    word_sentence_relation = {} #需要替换的<span class="hs_kw0_bestpl"></span>与下标的对应关系
    content_list = content.split('\t')
    for each_title_con_js in list_title_con_js: #依次读取list_title_con_js中每个模块，例如：最满意，最不满意
        each_title_list = each_title_con_js.split('|')  # 读取每个小标题的内容，并用\划分为list,[0]是标题，[1]是替换的文本，[2]是JS
        need_title = each_title_list[0]   #标题，例如最满意
        need_replaced_str = each_title_list[1] #需要被替换的文本
        need_uesed_js = each_title_list[2] #包含下标列表和文字编码列表，替换规则的JS
        print(need_uesed_js)#<script>(function(mg_){function FN_(){if (Bz_()) {if(hv_('ZZ_')=='ZZ_')... 若输出这种形式的为正常
        #对js进行提取，得到所需要的内容，index，code, 替换规则
        function_split = need_uesed_js.split('function')
        start = re.search(r']\(', function_split[3]).span()[1]   #这里报错，说明遇到了反扒，页面中需要验证，查看浏览器中页面或者多执行几次
        end = re.search('return', function_split[3]).span()[0]
        need_function = function_split[3][start: end]
        print(need_function) #''+pl_+HP_+gZ_+du_+WU_+Lr_+ig_+VS_+CJ_+Mx_+vE_+di_+rD_+xE_+jl_...若输出这种形式的为正常

        code_line_start_end = re.search(r'\);', need_function).span()
        need_word_code = need_function[:code_line_start_end[0]] #获取需要替换的文本编码  字母串''+pl_+HP_+gZ_+du_......
        print(need_word_code)

        index_need = need_function[code_line_start_end[1]:]
        index_need2 = index_need.split('=')[1]
        index_start = re.search(r'\(\(', index_need2).span()[1]
        index_end = re.search('\),', index_need2).span()[0]
        need_word_index = index_need2[index_start: index_end]  #获取对上述文本进行重排序的下标 字母串Jv_('')+''+Az_+yk_+YJ.....
        print(need_word_index)

        #获取自定义变量的替换规则并生成关系字典，例如：Fp_': "','", 'Mw_': "'1'"，用于替换上述Index 与 code
        #但此处时间复杂度会增加，原因：正则写的不够好，有待改进
        rule_need = (function_split)[-1]
        rule_sentence = re.search('}(.*?)}', rule_need).group(1)
        rule_split = rule_sentence.strip(' ').split('var') #匹配得到规则，并用list保存，例如['', " AC_='1'; ", " ae_='u'; ",.....]
        print(rule_split)
        #根据上述得到的规则，建立对应关系字典，
        for each_rule in rule_split[1:]:
            each_rule = each_rule.strip().strip(';').split('=')
            rule_dict[each_rule[0]] = each_rule[1]
        print(rule_dict) #对应规则，例如{'OL_': "'1'", 'Ig_': "','", 'aQ_': "';'",......}

        #重写代码，上述测试正确；2018.4.15.23.13
        #根据建立的变量替换规则替换混淆的index 和 code，得到正确的字体编码和重排序数组下标
        need_word_code_split = need_word_code.split('+')  #对混淆的文字串和下标串 以+进行分割
        need_word_index_split = need_word_index.split('+')
        need_word_code_changed = '' #字符串进行加前先定义
        need_word_index_changed = ''
        for each_word_code in need_word_code_split:
            if each_word_code in rule_dict:
                # print(i)
                need_word_code_changed += rule_dict[each_word_code].replace('\'','').strip()
        for each_word_index in need_word_index_split:
            if each_word_index in rule_dict:
                # print(i)
                need_word_index_changed += rule_dict[each_word_index].replace('\'','').strip()
        #输出结果中的，和；也是变量替换之后的结果，替换规则中包含这两个，正好可以用于在下一步中用这两项分割结果为list
        print(need_word_code_changed) #输出结果例如：eca2,ed04,edb7,ecbc,ed70,ed1e,eda6,edb6,ed8a,edbe,edf4,ed91,edc7,ec35,ec96,ecab,ed0d,ec64
        print(need_word_index_changed) #输出结果例如：3;6;17;10;15;7;14;0;13;12;2;4;8;11;1;16;9;5

        #将上文得到的下标与字体编码划分为list
        need_word_code_changed_list = need_word_code_changed.split(',')
        need_word_index_changed_list = need_word_index_changed.split(';')
        #将文字编码转为汉字
        for each_code in range(len(need_word_code_changed_list)):
            need_word_code_changed_list[each_code] = code_word_relation[need_word_code_changed_list[each_code]]
        print(need_word_code_changed_list)
        # 生成原文中顺序（根据index进行重排序后，原文中相同的文字只算一次）的下标与文字编码的的对应关系
        for each_index in range(len(need_word_index_changed_list)):
            index_word_relation[each_index] = need_word_code_changed_list[int(need_word_index_changed_list[each_index])]

        print('index_word_relation', index_word_relation)#例如{'3': '一', '4': '很', '1': '有',..}
        #重写代码，上述测试正确；2018.4.17.0.53

        #构造替换语句，进行替换，例如：替换<span class="hs_kw0_bestpl"></span>为空
        pattern = re.compile(r'<span class="hs_kw(.*?)_(.*?)">')
        result_list = re.findall(pattern, need_replaced_str)
        print(result_list)#[('0', 'bestpl'), ('1', 'bestpl'), ('2', 'bestpl'), ('3', 'bestpl')...]
        #生成替换语句与汉字的关系
        for each_find in result_list:
            word_sentence_relation[r'<span class="hs_kw' + each_find[0] + '_' + each_find[1] + '"></span>'] = index_word_relation[int(each_find[0])]
        print(word_sentence_relation)#{'<span class="hs_kw6_bestpl"></span>': '三', '<span class="hs_kw4_bestpl"></span>': '很',...}

        for key,value in word_sentence_relation.items():
            need_replaced_str = re.sub(key,value,need_replaced_str)
        print(need_replaced_str) #替换完之后的结果
        title_and_str = ':'.join([need_title, need_replaced_str])
        content_list.append(title_and_str)
        content = '\t'.join([content,title_and_str])

    print(content_list)
    print(content)
    return content

if __name__ == '__main__':

    #s = requests.session()
    #s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
    rule_dict_list = []

    #提取得到的所有链接文件路径
    link_path = r'G:\WorkSpace\python\Big_Crawer\crawer_qczj2\Q5_all_article_link.txt'
    link_list = get_link(link_path)  #保存在link_list中，等待遍历

    #测试时使用
    for j in range(41,len(link_list)):
        print(j, link_list[j]) #打印出具体个数与Link，以便报错时查看
        link = link_list[j] #得到Link
        content, list_title_con_js = get_content(link) #得到每个Link中需要的内容
        code_word_relation = get_code_word_relation()  # 生成自定义文字编码与文字的对应关系
        print(code_word_relation)

        content_total = get_replaced_content(content, list_title_con_js, code_word_relation)  #解析每个list_title_con_js
        write_txt(content_total, 'content_total.txt')

        time.sleep(10)
    # j = 34
    # x = 0
    # while (j <= len(link_list) ):
    #     try:
    #         # print(j, link_list[j])  # 打印出具体个数与Link，以便报错时查看
    #         # link = link_list[j]  # 得到Link
    #         # content, list_title_con_js = get_content(link)  # 得到每个Link中需要的内容
    #         # content_total = get_replaced_content(content, list_title_con_js)  # 解析每个list_title_con_js
    #         #
    #         # write_txt(content_total, 'content_total.txt')
    #
    #         print(j, link_list[j]) #打印出具体个数与Link，以便报错时查看
    #         link = link_list[j] #得到Link
    #         content, list_title_con_js = get_content(link) #得到每个Link中需要的内容
    #         code_word_relation = get_code_word_relation()  # 生成自定义文字编码与文字的对应关系
    #         print(code_word_relation)
    #
    #         content_total = get_replaced_content(content, list_title_con_js, code_word_relation)  #解析每个list_title_con_js
    #         write_txt(content_total, 'content_total.txt')
    #         j += 1
    #         time.sleep(5)
    #     except:
    #         link = link_list[j]
    #         time.sleep(10)
    #         x += 1
    #         if x >5:
    #             x = 0
    #             j += 1
    #             continue


'''
#完整的逻辑，可以使用，因为测试原因，放到末尾
while (j <= len(link_list)):
    print(j)
    print(link_list[j])
    try:
        link = link_list[j]
        content, list_title_con_js = get_content(link)
        get_real_content(list_title_con_js)

        for i in list_title_con_js:
            content = '\t'.join([content, i])
        print(content)
        write_txt(content, 'all_content.txt')
        content_list = content.split('\t')
        print(len(content_list), content_list)
        j += 1
        time.sleep(5)
    except:
        link = link_list[j]
        time.sleep(10)
    # break
'''
