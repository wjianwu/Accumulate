import requests
from lxml import etree
import xlrd
from xlwt import Workbook


def url_split(url):
    try:
        if constant_url[url] is not None:
            return constant_url[url]
    except KeyError:
        us = url.split("/")
        for u in us:
            if '.com' in u:
                constant_url[url] = u
                return u


def truth_title(url):
    try:
        if constant[url] is not None:
            print("旧URL，直接取出")
            return constant[url]
    except KeyError:
        r = requests.post(url).content
        text = etree.HTML(r)
        title = text.xpath('/html/head/title')
        constant[url] = title[0].text
        print("新URL，重新爬取")
        return title[0].text


def like_title(request_url, title):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/69.0.3497.100 Safari/537.36"
    }
    for i in range(10):
        url = request_url + "&pn=" + str(i * 10)
        with requests.get(url, headers=headers, timeout=10) as rg:
            e = etree.HTML(rg.text)
            content_list = e.xpath('//*[@id="content_left"]/div[contains(@class,"c-container")]')
            for contain in content_list:
                title_temp = contain.xpath("./h3/a")[0].xpath("string(.)")
                if title_temp[-3:] == "...":
                    title_temp = title_temp[:-3]
                if title_temp[:3] == "...":
                    title_temp = title_temp[3:]
                if title_temp in title:
                    return title
    return "无匹配(前后...已去掉)"


def read_csv(file_name):
    wb = xlrd.open_workbook(file_name)
    sheet = wb.sheet_by_index(0)
    rows = sheet.nrows
    return_list = []
    for i in range(rows - 1):
        # 读取表格数据
        keyword = sheet.row_values(i + 1)[0]
        url = sheet.row_values(i + 1)[1]
        # 获取真实地址的标题
        print("采集标题：" + url)
        title = truth_title(url)
        print("真实标题：" + title)
        print("开始访问关键字搜索标题----" + keyword)
        # 请求访问关键字链接
        request_url = "https://www.baidu.com/s?&rn=50&wd=" + keyword + "&si=" + url_split(url)
        # 获取匹配相似的标题
        rank_title = like_title(request_url, title)
        print(rank_title)
        # 存储关键字，原始链接，原始标题，爬取后标题页数或不存在
        single = [keyword, url, title, rank_title]
        return_list.append(single)
    return return_list


def save_excel(data):
    xls = Workbook(encoding='utf-8')
    sheet = xls.add_sheet('sheet_1')
    sheet.write(0, 0, "存储关键字")
    sheet.write(0, 1, "原始链接")
    sheet.write(0, 2, "原始标题")
    sheet.write(0, 3, "爬取后标题页数或不存在")
    for i in range(len(data)):
        for j in range(len(data[i])):
            sheet.write(i + 1, j, data[i][j])
    xls.save("C:\\Users\\wjianwu\\Desktop\\嘿嘿.xls")


constant = {}
constant_url = {}
result = read_csv('C:\\Users\\wjianwu\\Documents\\Tencent Files\\1336485920\\FileRecv\\哈哈.xlsx')
save_excel(result)
