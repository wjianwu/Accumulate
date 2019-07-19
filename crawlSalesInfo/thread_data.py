import threading

# 线程内全局变量
# local_data.new_links : 存放要爬取的网站
# local_data.complete_links : 存放已爬取完网站的顶级域名
# local_data.level : 存放爬取的层级，首次进入的为 1，通过友链进入累加 1，当前默认只爬取 5 层
# local_data.level_num : 当前层级所具有的网站个数
local_data = threading.local()
