import re

import requests
from lxml import etree


# 根据终端，引擎取相应的方法
from crawlSalesInfo.constants import Constants
from crawlSalesInfo.rule import qq_rule_names, phone_rule_names
from crawlSalesInfo.thread_data import local_data


def crawl_strategy(terminal_type, search_engine):
    if search_engine == "百度":
        if terminal_type == "PC":
            return crawl_sales_pc_baidu
        else:
            return crawl_sales_pc_baidu


# 根据行业取链接
def crawl_sales_pc_baidu(need_data):
    industry_name = need_data["industryName"]
    page_num = need_data["pageNum"]
    page_size = need_data["pagePerNum"]

    result = []
    for i in range(page_num):
        url = "http://www.baidu.com/s?wd=" + industry_name + "&pn=" + str(i * page_size) + "&rn=" + str(page_size)
        with requests.get(url, headers=Constants.headers, timeout=20) as resp:
            html = etree.HTML(resp.text)
            div_list = html.xpath("//div[@id='content_left']/div[contains(@class,'result')] | //div["
                                  "@id='unsafe_content']/div[contains(@class,'result')]")
            for div in div_list:
                try:
                    div_title = div.xpath(".//h3/a")[0].xpath("string(.)")
                    fast_act = div.xpath(".//div[contains(@class,'c-row c-gap-top-small')]/div[1]/div[1]/a |"
                                         " .//div[contains(@class,'f13')]/a")

                    fast_act_text = fast_act[1].xpath("string(.)")
                    if fast_act_text == "百度快照":
                        print(div_title)
                        result.append(fast_act[0].xpath("@href")[0])
                except:
                    print("############################################################-无效位置")
            print("--------------------------------------------------------------------第 " + str(i + 1) + " 页")
    print("-------------------")
    return result


# 获取权重
def get_power(link):
    try:
        url = 'http://baidurank.aizhan.com/baidu/' + link
        with requests.get(url) as resp:
            html = etree.HTML(resp.text)
            img = html.xpath("//li/img[@align='absmiddle']/@src")[0]
            return img[img.rfind('.') - 1:img.rfind('.')]
    except:
        print("获取权重失败->###############################" + link)
        return -1


# 响应编码处理
def object_decode(resp):
    text = ''
    for charset in Constants.charsets:
        try:
            text = resp.content.decode(charset)
            break
        except:
            continue
    if text == '':
        pre_encoding = resp.apparent_encoding.lower()
        if pre_encoding in Constants.charsets:
            resp.encoding = pre_encoding
        else:
            resp.encoding = 'utf-8'
        text = resp.text
    return text


# 获取标题
def get_title(resp):
    title = ''
    text = object_decode(resp)
    try:
        html = etree.HTML(text)
        title = html.xpath('//title')[0].xpath('string(.)')
    except:
        print("获取标题失败！>>>>>>>>>")
    return title


# 匹配规则
def match_rule(need_data, text):
    flag = True

    phones = re.findall(need_data["telReg"], text)
    # 普通匹配一次，需要判断是否含有 1[34578]\d{9} 规则
    for phone in phones:
        if len(phone) < 20:
            phone = phone.replace(' ', '')
        if re.findall('1[34578]\d{9}', phone):
            flag = False
            break

    if flag:
        # 上方没有，需采用指定的正则
        for rule_name in phone_rule_names:
            temp = eval(rule_name)(text)
            if len(temp) > 0:
                phones.extend(temp)
                flag = False
                break

    # 一般匹配的QQ号
    qqs = re.findall(need_data["qqReg"], text)
    # 采用指定的匹配规则
    for rule_name in qq_rule_names:
        temp = eval(rule_name)(text)
        qqs.extend(temp)
    # 没有采取到，则flag = True，代表要往'联系我们'中去匹配
    if len(qqs) == 0:
        flag = True

    return [phones, qqs, flag]


# 爬取信息
def get_call_info(resp, need_data):
    text = object_decode(resp)
    url = resp.url

    result = match_rule(need_data, text)
    phones = result[0]
    qqs = result[1]
    flag = result[2]

    result_one = [[], []]
    if flag:
        tuples = re.findall('(<[aA].*?>)(.*?)</[aA]>', text)
        for tup in reversed(tuples):
            if "联系我们" in tup[1] or "联系方式" in tup[1] or "联络我们" in tup[1]:
                href = re.findall('href="(.*?)"', tup[0])[0]
                if href[0:2] == "//":
                    href = "http:" + href
                if "http" not in href:
                    if href[0:1] == "/":
                        href = url + href[1:]
                    else:
                        href = url + href
                with requests.get(href, headers=Constants.headers, timeout=20) as about_us_arg:
                    about_us_text = ''
                    for charset in Constants.charsets:
                        try:
                            about_us_text = about_us_arg.content.decode(charset)
                            break
                        except:
                            continue
                    if about_us_text == '':
                        about_us_arg.encoding = 'utf-8'
                        about_us_text = about_us_arg.text
                    result_one = match_rule(need_data, about_us_text)
                break
    phones.extend(result_one[0])
    qqs.extend(result_one[1])

    # 数据去重
    phones = repeat_data(phones)
    qqs = list(set(qqs))
    if len(phones) > 5:
        phones = phones[0:5]
    if len(qqs) > 5:
        qqs = qqs[0:5]
    phones_qqs = [str(phones), str(qqs)]

    realm = get_realm_name(url, '//.*?/|//.*')  # 保存已爬取完url的顶级域名在 complete_links
    if realm not in local_data.complete_links:
        local_data.complete_links.append(realm[1])

    # 爬取友链
    dim_links = re.findall('<a href=[\'"]http[s]?://.*?</a>', text)
    for dim_link in dim_links:  # 遍历所有<a>标签
        main_text = re.findall(">.*</a>", dim_link)  # 获取<a>标签的内容
        if len(main_text) != 0 and need_data["industryName"] in main_text[0]:  # <a>标签的内容必须包含有行业词
            realm_name = get_realm_name(dim_link, '//.*?[/"\']|//.*')  # 提取友链的域名 + 顶级域名
            if realm_name[0] not in local_data.new_links and realm_name[1] not in local_data.complete_links and \
                    realm_name[2] != 'm':
                local_data.new_links.append(realm_name[0])
    return phones_qqs


# 获取域名 + 顶级域名
def get_realm_name(string, reg):
    try:
        result = []
        realm_name = re.findall(reg, string)[0]
        if realm_name[-1] == "/" or realm_name[-1] == "\"" or realm_name[-1] == "\'":
            realm_name = realm_name[2:-1]
        else:
            realm_name = realm_name[2:]
        result.append(realm_name)

        realm_name = realm_name.lower()  # 转小写

        chips = realm_name.split(".")
        if chips[-2] in ['com', 'cn', 'org', 'net']:
            top_realm_name = chips[-3] + "." + chips[-2] + "." + chips[-1]
        else:
            top_realm_name = chips[-2] + "." + chips[-1]
        result.append(top_realm_name)
        result.append(chips[0])
        return result
    except:
        print("获取友链时，分离域名及顶级域名时异常！###############")


# 去重，去掉空和相同号码，切割一行多个号码
def repeat_data(phones):
    contains = []
    check = []
    for phone in phones:
        chips = re.split('[:：]', phone)
        if len(chips) == 1 or len(chips[1]) < 8:
            continue
        if len(chips[1]) > 20:
            temp = re.split('[ ,，]', chips[1])
            for t in temp:
                if t == '':
                    continue
                else:
                    check.append(t.strip())
                    contains.append(chips[0] + '：' + t)
        else:
            check.append(chips[1].strip())
            contains.append(phone)
    result = []
    check = list(set(check))
    for c in check:
        for contain in contains:
            if c in contain:
                result.append(contain)
                break
    return result
