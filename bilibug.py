#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup
import datetime
import time
import urllib.request
import re
import pandas as pd
from google.appengine.api import mail


def getavlist(urlpage):
    #从静态网页获得视频av号列表
    page=urllib.request.urlopen(urlpage)
    soup=BeautifulSoup(page,'html.parser')
    txtcont=soup.find('div',{'class':'txtcont'})
    txtcont=str(txtcont)
    av_list=re.findall('<p.*?(\d+).*?</p>',txtcont,re.S)
    av=av_list[::-1]
    return av


def getdaystr():
    #获得时间格式
    today=datetime.datetime.now()
    oneday=datetime.timedelta(days=1)
    yesterday=today-oneday
    yesterdaystr=yesterday.strftime('%Y-%m-%d')
    nowstr=today.strftime('%Y-%m-%d %H:%M:%S')
    return yesterdaystr,nowstr



def getdata(av_list):
    #获得数据
    L1=[ ]
    L2=[ ]
    [yesterdaystr,nowstr]=getdaystr()
    row=0
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    for avid in av_list:
        r = requests.get(url='https://api.bilibili.com/x/web-interface/archive/stat?aid='+avid, headers=headers)
        j=r.json()['data']
        aid=j['aid']
        view=j['view']
        danmaku=j['danmaku']
        reply=j['reply']
        favorite=j['favorite']
        coin=j['coin']
        share=j['share']
        like=j['like']
        beizhu=''
        t1=[aid,'danmaku','reply','favorite','coin','share','like','beizhu']
        t2=[view,danmaku,reply,favorite,coin,share,like,beizhu]
        L1=L1+t1
        L2=L2+t2
    return L1,L2


def send_mail(to,sub,context):
      mail.send_mail('blackgundamwyr@gmail.com',
       'me<black_gundam@163.com',
       sub, 
       'rt',
       html =context)
    return

def convertToHtml(result,title):
    #将数据转换为html的table
    #result是list[list1,list2]这样的结构
    #title是list结构；和result一一对应。titleList[0]对应resultList[0]这样的一条数据对应html表格中的一列
    d = {}
    index = 0
    for t in title:
        d[t]=result[index]
        index = index+1
    df = pd.DataFrame(d)
    df = df[title]
    h = df.to_html(index=False)
    html="""<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<body>
<div id="content">
"""+h+"""
</div>
</div>
</body>
</html>
"""
    return html

def bilibug(urlpage):
    [yesterdaystr,nowstr]=getdaystr()
    av_list=getavlist(urlpage)
    [L1,L2]=getdata(av_list) 
    mailto="black_gundam@163.com"
    sub=yesterdaystr+"影思B站数据 采集于"+nowstr
    result = [L1,L2]
    title = ['视频编号',yesterdaystr]
    html=convertToHtml(result,title)
    context = MIMEText(html,_subtype='html',_charset='utf-8') 
    send_mail(mailto,sub,context)
    return


if __name__ == '__main__':
    urlpage='http://blackgundam.lofter.com/post/2f0990_12dd602bb'
    bilibug(urlpage)
   


