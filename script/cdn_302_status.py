#!/usr/bin/env python

#cdn每个302节点返回状态

import http.client
import hashlib
from urllib import parse

url_list=["http://xxxxx:8080/000000001001/3000000001000005308/3000000001000005308.m3u8?channel-id=FifastbLive&livemode=1&Contentid=3000000001000005308&stbId=toShengfenFIFA&usergroup=g28093100000",
          "http://xxxxx:8080/000000001001/3000000001000028638/3000000001000028638.m3u8?channel-id=FifastbLive&livemode=1&Contentid=3000000001000028638&stbId=toShengfenFIFA&usergroup=g28093100000"]
def url_parse(url):
    dict_url = {}
    result = parse.urlparse(url)
    host = result.netloc
    path = result.path
    query = result.query
    dict_url["host"] = host
    dict_url["path"] = path
    dict_url["query"] = query
    return dict_url


for url in url_list:
    result={}
    while True:
        a = url_parse(url)
        host = a["host"]
        path = a["path"]
        query = a["query"]
        conn=http.client.HTTPConnection(host,timeout=5)
        conn.request("GET",path + "?" + query)
        response=conn.getresponse()  #获取CDN的回应内容信息
        stat = response.status     #输出http状态码
        head=response.getheaders()  #打印回应头信息，以列表嵌元组的方式表示
        body = response.read()
        conn.close()
        if stat == 302:
            for i in head:
                 if "Location" in i:
                    url=i[1]
                    #print(host,stat,path)
                    #print("host:%-30s stat:%-8s path:%-100s"%(host,stat,path))
                    result[host]=stat


        else:
            #print(host,stat,path)
            #print("host:%-30s stat:%-8s path:%-100s"%(host,stat,path))
            result[host]=stat
            print(result)
            break
