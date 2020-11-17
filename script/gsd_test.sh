#!/usr/bin/env python
#gsd 压力测试

import httplib
import time
import os

httpClient = None

if os.path.exists('result'):
    os.remove('result')

if os.path.exists('result-fail'):
    os.remove('result-fail')

def status():
    file = open('id')
    line = file.readlines()
    file.close()
    for i in line:
        try:
            httpClient = httplib.HTTPConnection('x.x.x.x',8000,timeout=10)
            req = "/xxxx.m3u8?channel-id=bstvod&Contentid=" + i.strip() + "&stbId=12345678&owsid=123"
            httpClient.request("GET", req)
            response = httpClient.getresponse()
            status = response.status
            head = response.getheaders()
            print  str(status),
            print head[1][1] 
            result = open("result" ,'a+')
            result.write(str(status) + ' ')
            result.write(head[1][1] + '\n')
            result.close()
            time.sleep(0.005)
        except Exception as e:
            print e
            resultfail = open("result-fail" ,'a+')
            resultfail.write(str(e) + '\n')
            resultfail.close()
while True:
    time.sleep(0.005)
    status()
