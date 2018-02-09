#coding=utf-8
import urllib2
from bs4 import BeautifulSoup
import csv


def IPspider(numpage):
    csvfile = file('ips.csv', 'wb')
    writer = csv.writer(csvfile)
    url = 'http://www.xicidaili.com/nn/'
    user_agent = 'IP'
    headers = {'User-agent': user_agent}
    for num in xrange(1, numpage + 1):
        ipurl = url + str(num)
        print 'Now downloading the ' + str(num * 100) + ' ips'
        request = urllib2.Request(ipurl, headers=headers)
        content = urllib2.urlopen(request).read()
        bs = BeautifulSoup(content, 'html.parser')
        res = bs.find_all('tr')
        for item in res:
            try:
                temp = []
                tds = item.find_all('td')
                temp.append(tds[1].text.encode('utf-8'))
                temp.append(tds[2].text.encode('utf-8'))
                writer.writerow(temp)
            except IndexError:
                pass

                # 假设爬取前十页所有的IP和端口
IPspider(10)

import socket

def IPpool():
    socket.setdefaulttimeout(2)
    reader=csv.reader(open('ips.csv'))
    IPpool=[]
    for row in reader:
        proxy=row[0]+':'+row[1]
        proxy_handler=urllib2.ProxyHandler({"http":proxy})
        opener=urllib2.build_opener(proxy_handler)
        urllib2.install_opener(opener)
        try:
            html=urllib2.urlopen('http://www.baidu.com')
            IPpool.append([row[0],row[1]])
        except Exception,e:
            continue
    return IPpool

IPpool();