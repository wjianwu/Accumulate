import requests

from crawlSalesInfo.constants import Constants


def get_industry_name():
    params = {"username": Constants.username, "password": Constants.password}
    url = Constants.host + "/external/industry/getValidIndustryInfo"
    need_data = None
    try:
        with requests.post(url=url, json=params, timeout=60) as re:
            if re.status_code == requests.codes.ok:
                need_data = re.json()
                print("-----------------------------当前词：" + need_data["industryName"] + "-----------------------------")
    except:
        print("------------------------------------获取数据失败------------------------------------")
    finally:
        return need_data


def return_data(result):
    result["userName"] = Constants.username
    result["password"] = Constants.password
    url = Constants.host + "/external/industry/updateIndustryInfoDetail"
    # url = "http://localhost:8888/account/feedback"
    try:
        with requests.post(url=url, json=result, timeout=60) as re:
            if re.status_code == requests.codes.ok:
                print("------------------------------成功返回数据结果------------------------------")
            else:
                print("------------------------------返回数据结果失败------------------------------")
    except:
        print("----------------------------------返回数据结果异常----------------------------------")


def complete(uuid):
    result = {"username": Constants.username, "password": Constants.password, "uuid": str(uuid)}
    url = Constants.host + "/external/industry/updateIndustryInfoStatus"
    try:
        with requests.post(url=url, json=result, timeout=60) as re:
            if re.status_code == requests.codes.ok:
                print("------------------------------成功修改完成状态------------------------------")
            else:
                print("------------------------------修改完成状态失败------------------------------")
    except:
        print("----------------------------------修改完成状态异常----------------------------------")
