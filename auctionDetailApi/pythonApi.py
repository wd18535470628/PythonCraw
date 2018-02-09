#coding=utf-8
from flask import Flask,request
import urllib2,re
import json
from mysql import Mysql
mysql = Mysql()

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'hello world'

@app.route('/getDetail', methods=['POST'])
def register():
    type = eval(request.data)['platform']
    url = eval(request.data)['url']
    if type == 'tb':
        my_dict = getTbContents(url)
        mysql.insertTbData('auction_id','auction_detail',my_dict)
    elif type == 'jd':
        my_dict = getJdContents(url)
        mysql.insertJdData('api_auction_id','api_auction_detail',my_dict)
    return json.dumps(my_dict,encoding="UTF-8", ensure_ascii=False, sort_keys=False, indent=4)
def getTbContents(url):
    my_dict = {}
    page = getTbPage(url)
    my_dict['enrollment'] = re.findall(re.compile(r'class="J_Applyer">(.*?)</em>',re.S), page).__len__() > 0 and unicodeToStr(re.findall(re.compile(r'class="J_Applyer">(.*?)</em>',re.S), page)[0]) or ""
    my_dict['onlookers'] = re.findall(re.compile(r'id="J_Looker">(.*?)</em>',re.S),page).__len__() >0 and unicodeToStr(re.findall(re.compile(r'id="J_Looker">(.*?)</em>',re.S),page)[0]) or ""
    my_dict['auction_id'] = re.findall(re.compile(r'sf_item/(.*?).htm', re.S), page).__len__() > 0 and unicodeToStr(re.findall(re.compile(r'sf_item/(.*?).htm', re.S), page)[0]) or ""
    my_dict['auction_name'] = re.findall(re.compile(r'<h1>(.*?)\r\n',re.S), page).__len__() > 0 and unicodeToStr(re.findall(re.compile(r'<h1>(.*?)\r\n',re.S), page)[0]) or ""
    my_dict['current_price'] = re.findall(re.compile(r'<span class="pm-current-price J_Price">\n\t\t\t\t<em>(.*?)</em>',re.S), page).reunicodeToStr(re.findall(re.compile(r'<span class="pm-current-price J_Price">\n\t\t\t\t<em>(.*?)</em>',re.S), page)[0])
    priceList = re.findall(re.compile(r'J_Price">(.*?)</span>', re.S), page)[1:]
    my_dict['start_price'] = unicodeToStr(priceList[0])
    my_dict['fare_increase'] = unicodeToStr(priceList[1])
    my_dict['cash_deposit'] = unicodeToStr(priceList[2])
    my_dict['access_price'] = unicodeToStr(priceList[3])
    my_dict['pay_type'] = re.findall(re.compile(r'<span class="pay-type">(.*?)</span>', re.S),page).__len__() > 0 and unicodeToStr(re.findall(re.compile(r'<span class="pay-type">(.*?)</span>', re.S),page)[0]) or ""
    my_dict['bidding_cycle'] = unicodeToStr(re.findall(re.compile(r'<span>:(..[^\x00-\xff]{1}.*?)</span>'),page)[0])
    my_dict['delay_cycle'] = unicodeToStr(re.findall(re.compile(r'<span>.(.*?)<span class="pay-type-help"></span>'),page)[0])
    #限购
    list = re.findall('pai-tag tag-buy-restrictions J_Tag',page)
    if list.__len__() == 0:
        my_dict['limit_pay'] = "1"
    else:
        my_dict['limit_pay'] = "0"
    #正在进行
    list = re.findall('status-ing',page)
    if list.__len__() == 0:
        list = re.findall('status-tip', page)
        if list.__len__() == 0:
            my_dict['status'] = "2"
        else:
            my_dict['status'] = "0"
    else:
        my_dict['status'] = "1"
    my_dict['end'] = unicodeToStr(re.findall(re.compile(r'countdown J_TimeLeft">(.*?)</span>'),page)[0])
    my_dict['disposal_court'] = unicodeToStr(re.findall(re.compile(r'<a target="_blank" href="//sf.taobao.com/[0-9]{1,5}/[0-9]{1,5}">(.*?)</a>', re.S), page)[0])
    my_dict['contact'] = ""
    for str in re.findall(re.compile(r'class="pai-info".*?(1[34578]\d{9}/[0-9]{3,4}-[0-9]{7,8}|[0-9]{3,4}-[0-9]{7,8}|0\d{2,3}\d{7,8}|1[358]\d{9}|147\d{8}).*?</p>', re.S), page):
        my_dict['contact'] = my_dict['contact'] + "/" +unicodeToStr(str)
    my_dict['contact'] = my_dict['contact'][1:]
    my_dict['set_reminders'] = unicodeToStr(re.findall(r'<em>([0-9]{1,5})</em>',page)[0])
    my_dict['linkman'] = unicodeToStr(re.findall(re.compile(r'class="pai-info".*?([^\x00-\xff]{2,4}|[^\x00-\xff]{2,4} [^\x00-\xff]{2,4})</em>', re.S), page)[0])
    return my_dict
def getJdContents(url):
    my_dict = {}
    my_dict = getJdQueryAccess(url,my_dict)
    my_dict = getJdData(url,my_dict)
    return my_dict
def getTbPage(url):
    user_agent = '"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36"'
    headers = {'User-Agent': user_agent}
    maxTryNum = 10
    for tries in range(maxTryNum):
        try:
            req = urllib2.Request(url, headers=headers)
            html = urllib2.urlopen(req).read()
            break
        except:
            if tries < (maxTryNum - 1):
                continue
            else:
                print "Has tried %d times to access url %s, all failed!", maxTryNum, url
                break
    return html.decode('gbk')
def getJdQueryAccess(url,my_dict):
    user_agent = '"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36"'
    headers = {'User-Agent': user_agent}
    my_dict['id'] = str(re.findall(re.compile(r'[0-9]{8,11}'), url)[0])
    url = 'https://paimai.jd.com/json/ensure/queryAccess?t=613189sku=19133180010&paimaiId='+ my_dict['id']
    maxTryNum = 10
    for tries in range(maxTryNum):
        try:
            req = urllib2.Request(url, headers=headers)
            html = urllib2.urlopen(req).read()
            break
        except:
            if tries < (maxTryNum - 1):
                continue
            else:
                print "Has tried %d times to access url %s, all failed!", maxTryNum, url
                break
    my_dict['query_access'] = str(json.loads(html)['accessEnsureNum'])
    return my_dict
def getJdData(url,my_dict):
    user_agent = '"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36"'
    headers = {'User-Agent': user_agent}
    my_dict['id'] = str(re.findall(re.compile(r'[0-9]{8,11}'), url)[0])
    url = 'https://paimai.jd.com/json/current/englishquery?paimaiId='+ my_dict['id'] +'&skuId=0&t=775839&start=0&end=9'
    maxTryNum = 10
    for tries in range(maxTryNum):
        try:
            req = urllib2.Request(url, headers=headers)
            html = urllib2.urlopen(req).read()
            break
        except:
            if tries < (maxTryNum - 1):
                continue
            else:
                print "Has tried %d times to access url %s, all failed!", maxTryNum, url
                break
    temp = json.loads(html)
    my_dict['bid_count'] = str(temp['bidCount'])
    if temp['auctionStatus'] == '0':
        my_dict['auction_status'] = '0'
    elif temp['auctionStatus'] == '1':
        my_dict['auction_status'] = '1'
    elif temp['auctionStatus'] == '2':
        if temp['displayStatus'] == '1':
            if temp['bidCount'] == '0':
                my_dict['auction_status'] = '8'
            elif temp['bidCount'] != '0':
                my_dict['auction_status'] = '2'
        else:
            my_dict['auction_status'] = temp['auctionStatus']
    my_dict['current_price'] = str(temp['currentPrice'])
    return my_dict
def unicodeToStr(unicode):
    return str(unicode.decode("utf-8").encode("utf-8").replace(",",""))

if __name__ == '__main__':
    app.run(port=8080,debug='true')