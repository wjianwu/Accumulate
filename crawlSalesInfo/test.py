import requests


from crawlSalesInfo.constants import Constants
from crawlSalesInfo.util import get_call_info

new_link = 'http://www.scjianzhan.cn/'
need_data = {
    'telReg': '电 *话[号]?[码]? *[:：] *[( )+\d-]+|'
              '手 *机 *[:：] *[( )+\d-]+|'
              '热 *线 *[:：] *[( )+\d-]+|'
              '直 *线 *[:：] *[( )+\d-]+|'
              '.女 *士 *[:：] *[( )+\d-]+|'
              '.经 *理 *[:：] *[( )+\d-]+',
    'qqReg': '[Qq] *[Qq] *[:：] *\d{8,10}',
    'industryName': 'LED'
}
with requests.get(new_link, headers=Constants.headers, timeout=20) as resp:
    result = get_call_info(resp, need_data)
