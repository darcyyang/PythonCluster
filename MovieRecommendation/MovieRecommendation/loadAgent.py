# -*- coding: utf-8 -*-

import requests
from lxml import etree,html
import re
from MovieRecommendation import myConfig
# import datetime
from time import gmtime, strftime
class agentLoader():

        def __init__(self):
            self.mockheaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
                           'Accept-Encoding': 'gzip, deflate',
                           'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                           'Connection': 'keep-alive',
                           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                           # 'Cookie':'bid="+C+9xhDdviA"; __utma=30149280.1224461064.1435281944.1464587297.1464594976.7; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1464594974%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Dn5dIXOIZj94QFE0XY1JUEM5YYA8Y9YG3F7PrIBBVFxdTpVcA8eIqjero539ZeRcs%26wd%3D%26eqid%3D8b7a2eb6000534e40000000557470f0f%22%5D; _pk_id.100001.4cf6=b9a74c2e618bd6ce.1464274710.5.1464594996.1464587295.; ap=1; __utmc=30149280; __utmz=30149280.1464576168.4.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.1511161292.1464576168.1464587297.1464594976.4; __utmc=223695111; __utmz=223695111.1464576168.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _pk_ses.100001.4cf6=*; __utmb=30149280.0.10.1464594976; __utmb=223695111.0.10.1464594976; dbcl2="4020511:YIGQcP71V6Q"; ck=3CcL'
                           }
            self.results = []

        def execute(self):
            self.get_valid_proxies(self.get_proxies_from_site(), myConfig.num_of_agent)
            if self.results != None and len(self.results) > 0:
                self.fileWriter(self.results)
                print 'get ' + str(len(self.results)) + ' proxies'

        def get_proxies_from_site(self):
            url = 'http://proxy.ipcn.org/proxylist.html'
            xpath = '/html/body/table/tr/td/pre/text()'

            r = requests.get(url,headers=self.mockheaders)
            content = html.fromstring(r.content)
            tree = etree.HTML(r.content)
            results1 = content.xpath(xpath)
            results = tree.xpath(xpath)
            proxies = results[0].split('\n')
            # proxies = [line.strip() for line in results]
            return proxies


        def checkProxyRule(self,proxy):

           return re.match('(?:[01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.(?:[01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.(?:[01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.(?:[01]?\\d\\d?|2[0-4]\\d|25[0-5])',proxy)

        #使用http://lwons.com/wx网页来测试代理主机是否可用
        def get_valid_proxies(self,proxies, count):
            url = 'http://google.com'
            cur = 0
            for p in proxies:
                patternStr = self.checkProxyRule(p)
                if patternStr != None:
                    succeed = self.checkProxy(p,url)
                    if succeed:
                        print 'succeed:', p
                        self.results.append(p)
                        cur += 1
                        if cur >= count:
                            break


        def checkProxy(self,proxyStr,url):
            proxy = {'http': 'http://' + str(proxyStr)}
            succeed = False
            try:
                r = requests.get(url, proxies=proxy,headers=self.mockheaders)
                if r.text == 'default':
                    succeed = True
            except Exception, e:
                print 'error:', proxy
                succeed = False
            if succeed:
                print 'succeed:', proxy


        def fileWriter(self,results):
            f = open(myConfig.agent_generate_file, 'w')
            f.write('#update the proxy at ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '\n')
            for proxy in results:
                f.write('http://' + proxy + '\n')
            f.close()


# print checkProxyRule('192.168.1.1:8080')
agentLoader().execute()