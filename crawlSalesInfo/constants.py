from configparser import ConfigParser


class Constants:
    cf = ConfigParser()
    cf.read(filenames='config.ini', encoding='utf-8-sig')

    host = "http://pcsskjlocal.shunshikj.com:80"
    username = "duchengfu"
    password = "test"
    crawl_level = 5
    default_filter = ['baidu.com', 'jd.com', 'tmall.com']
    default_threading = 1

    try:
        custom = cf.get('set', 'custom')
        if custom:
            print("<<<----启用配置文件中的配置---->>>")
            host = cf.get('connect', 'request_host')
            username = cf.get('connect', 'request_username')
            password = cf.get('connect', 'request_password')
            crawl_level = int(cf.get('set', 'crawl_level'))
            default_filter = cf.get('set', 'default_filter').split(',')
            default_threading = int(cf.get('set', 'default_threading'))
    except:
        print("<<<----读取配置文件config.ini失败，启动默认配置---->>>")

    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/55.0.2883.87 Safari/537.36 "
    }

    charsets = ['gb2312', 'utf-8', 'gbk']
