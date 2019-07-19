import requests
from lxml import etree

with requests.get(url="https://www.baidu.com/s?wd=seo&pn=0&rn=10", headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/69.0.3497.100 Safari/537.36"
}, timeout=10) as f:
    html = etree.HTML(f.text)
    div_list = html.xpath('//*[@id="content_left"]/div[contains(@class,"c-container")]')
    for div in div_list:
        print(div.xpath("@data-click")[0])
