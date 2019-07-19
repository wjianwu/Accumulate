import threading
import time

import requests

from crawlSalesInfo.constants import Constants
from crawlSalesInfo.service import get_industry_name, complete, return_data
from crawlSalesInfo.thread_data import local_data
from crawlSalesInfo.util import crawl_strategy, get_realm_name, get_call_info, get_title


def crawl_data():
    try:
        need_data = get_industry_name()
        # 取不到词，直接返回
        if need_data is None:
            local_data.new_links = []
            local_data.complete_links = []
            return None
        # 直接根据词取排名网站
        if need_data["targetUrl"] is None or need_data["targetUrl"] == '':
            function_name = crawl_strategy(need_data["terminalType"], need_data["searchEngine"])
            links = function_name(need_data)
            local_data.new_links = links
        # 从给定的起始网站开始
        else:
            local_data.new_links = [need_data["targetUrl"]]
        local_data.complete_links = []
        # 初始化层级以及当前层级数
        local_data.level_num = len(local_data.new_links)
        local_data.level = 1
        return need_data
    except:
        print("error-----error-----error-----访问中断-----error-----线程重启-----error-----error-----error-----")
        # 线程重启
        threading.Thread(target=get_crawl_info).start()


def get_crawl_info():
    need_data = crawl_data()
    while True:
        if need_data is None:
            print("@@@@@@@@@@@@@@@@@@@@@@@@-60s-@@@@@@@@@--暂无可获取的行业--@@@@@@@@@--60s--@@@@@@@@@@@@@@@@@@@@@@@@")
            time.sleep(60)
            need_data = crawl_data()
            continue
        # 层级限制，default = 5
        if local_data.level > Constants.crawl_level:
            local_data.new_links = []
        # 完成爬取
        if len(local_data.new_links) == 0:
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-60s-@@@@@@@@@--END--@@@@@@@@@--60s--@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            complete(need_data["uuid"])
            time.sleep(60)
            need_data = crawl_data()
            continue
        new_link = local_data.new_links[0]
        local_data.new_links.remove(new_link)
        # 层级计算
        if local_data.level_num != 0:
            local_data.level_num = local_data.level_num - 1
        else:
            local_data.level_num = len(local_data.new_links)
            local_data.level = local_data.level + 1

        if 'http' not in new_link:
            new_link = 'http://' + new_link
        print("访问链接---->" + new_link)
        try:
            with requests.get(new_link, headers=Constants.headers, timeout=20) as resp:
                print("网站：" + resp.url)
                realm = get_realm_name(resp.url, '//.*?/|//.*')
                # 过滤掉指定链接，可在config.ini中配置
                if realm[1] not in Constants.default_filter:
                    result = get_call_info(resp, need_data)
                    info = {
                        "title": get_title(resp),
                        "phones": result[0],
                        "qqs": result[1],
                        # "weight": get_power(realm[0]),
                        "weight": -1,
                        "website": resp.url,
                        "level": local_data.level,
                        "industryID": need_data["uuid"]
                    }
                    print("结果返回：" + str(info))
                    # 返回结果
                    return_data(info)
                else:
                    print("##############自动过滤掉链接：" + realm[1])
        except:
            print("访问出错")


if __name__ == '__main__':
    for i in range(Constants.default_threading):
        threading.Thread(target=get_crawl_info).start()
        time.sleep(2)
