import json
import random
import time
import requests
import chardet
from lxml import etree
from requests.exceptions import ConnectionError

user_agents = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
    # iPhone 6：
    "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",

]


class GetProxy():

    def __init__(self):
        self.headers = {"User-Agent": random.choice(user_agents)}

    # 判断提供ip代理网站是否有效，返回网页html文档
    def parse_url(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.encoding = chardet.detect(response.content)["encoding"]
            if response.status_code == 200:
                return response.text
            else:
                return None
        except ConnectionError:
            print("Error.")
        return None

    # 获取西刺代理网站免费代理ip
    def xici_proxy(self):
        # 加入延时，防止ip被封
        time.sleep(3)
        # 只获取网站高匿代理前20页的代理
        # xici_list = list()
        for i in range(1, 20):
            url = "https://www.xicidaili.com/nn/{}".format(i)
            response = self.parse_url(url)
            # 上面的response类型有时候是NoneType,有些是str，下面使用str(response)
            html = etree.HTML(str(response), etree.HTMLParser())
            # 所有的ip和port都是放在属性为ip_list标签下的tr标签里面
            # ip_list属性唯一，下面两种方式都是选取所有属性id='ip_list'的标签
            ip_list = html.xpath("//table[@id='ip_list']/tr/td[2]/text()")
            port_list = html.xpath("//*[@id='ip_list']/tr/td[3]/text()")

            # ip和port生成一个一一对应的元组列表，然后取出
            for ip, port in zip(ip_list, port_list):
                proxy = ip + ":" + port
                proxy = {"proxy": proxy}  # 返回的代理是字典的格式，方便直接存储到mongodb数据库中
                yield proxy
                # xici_list.append(proxy)
        # return xici_list

    # 获取快代理网站免费代理ip
    def kuai_proxy(self):
        # 加入延时
        time.sleep(3)
        # 只获取网站高匿代理前20页的代理
        # kuai_list = list()
        for i in range(1, 20):
            url = "https://www.kuaidaili.com/free/inha/{}/".format(i)
            response = self.parse_url(url)
            # 上面的response类型有时候是NoneType,有些是str，下面使用str(response)
            html = etree.HTML(str(response), etree.HTMLParser())
            # 所有的ip和port都是放在属性为list的div/table/tbody下的tr标签里面
            ip_list = html.xpath("//div[@id='list']/table/tbody/tr/td[1]/text()")
            port_list = html.xpath("//div[@id='list']/table/tbody/tr/td[2]/text()")

            # ip和port生成一个一一对应的元组列表，然后取出
            for ip, port in zip(ip_list, port_list):
                proxy = ip + ":" + port
                proxy = {"proxy": proxy}  # 返回的代理是字典的格式，方便直接存储到mongodb数据库中
                yield proxy
                # kuai_list.append(proxy)
        # return kuai_list

    # 获取快代理网站免费代理ip
    def liuliu_proxy(self):
        # 只获取网站高匿代理前20页的代理
        # liuliu_list = list()
        for i in range(1, 20):
            # 加入延时
            time.sleep(3)
            url = "http://www.66ip.cn/{}.html".format(i)
            response = self.parse_url(url)
            # 上面的response类型有时候是NoneType,有些是str，下面使用str(response)
            html = etree.HTML(str(response), etree.HTMLParser())
            # 所有的ip和port都是放在属性为list的div/table/tbody下的tr标签里面,列表第一个元素是标题栏，去除掉
            ip_list = html.xpath("//div[@class='containerbox boxindex']/div[1]/table[1]//tr/td[1]/text()")[1:]
            port_list = html.xpath("//div[@class='containerbox boxindex']/div[1]/table[1]//tr/td[2]/text()")[1:]

            # ip和port生成一个一一对应的元组列表，然后取出
            for ip, port in zip(ip_list, port_list):
                proxy = ip + ":" + port
                proxy = {"proxy": proxy}  # 返回的代理是字典的格式，方便直接存储到mongodb数据库中
                yield proxy
                # liuliu_list.append(proxy)
        # return liuliu_list

    # 自己可以扩充代理网站
    def other_proxy(self):
        headers = {"User-Agent": random.choice(user_agents)}
        url = 'http://proxylist.fatezero.org/proxy.list'
        proxy_list = list()
        r = requests.get(url, headers=headers)
        if r.raise_for_status() is None:
            # print(r.text)
            data = r.text.split('\n')
            # print(data[0])
            # print(len(data))
            for i in range(len(data) - 1):
                ip = json.loads(data[i])['host']
                port = json.loads(data[i])['port']
                proxy = str(ip) + ":" + str(port)
                proxy = {"proxy": proxy}  # 返回的代理是字典的格式，方便直接存储到mongodb数据库中
                yield proxy


if __name__ == '__main__':
    res = GetProxy().other_proxy()
    print(res)
    for i in res:
        print(type(i))
        print(i)
