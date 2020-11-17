#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import httplib
import hashlib
from urlparse import urlparse


base_url = "http://xxx.xxx.cmvideo.cn/index.m3u8?livemode=1&Contentid=300000000108&stbId=12345&usergroup=g28093100000&channel-id="


channel_list = ['cmcc','test']

def url_parse(url):
    dict_url = {}
    result = urlparse(url)
    host = result.netloc
    path = result.path
    query = result.query
    dict_url["host"] = host
    dict_url["path"] = path
    dict_url["query"] = query
    return dict_url


for channel in channel_list:
    url = '%s%s' %  (base_url,channel)
    #print(url)
    result={}
    parse_res = url_parse(url)
    host = parse_res["host"]
    path = parse_res["path"]
    query = parse_res["query"]
    conn=httplib.HTTPConnection(host,timeout=5)
    conn.request("GET",path + "?" + query)
    response=conn.getresponse()  #获取CDN的回应内容信息
    stat = response.status     #输出http状态码
    head=response.getheaders()  #打印回应头信息，以列表嵌元组的方式表示
    body = response.read()
    conn.close()
    result['host'] = host
    result['stat'] = stat
    result['channel-id'] = channel
    if stat == 302:
        for i in head:
            if "location" in i:
                location_url=i[1]
                location_parse = url_parse(location_url)
                result['location_host'] = location_parse['host']
    
    if stat != 302: 
        print("\033[1;31;44m入口域名: %-30s 频道: %-30s 状态码: %-8s 出口域名: %-50s\033[0m"%(result['host'],result['channel-id'],result['stat'],result.get('location_host','None')))
    else:
        print("入口域名: %-30s 频道: %-30s 状态码: %-8s 出口域名: %-50s"%(result['host'],result['channel-id'],result['stat'],result.get('location_host','None')))
