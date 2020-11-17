#!/usr/bin/env python
#coding=utf-8

#查询ip地理位置

import re
import requests


#内网情况下需要配置代理
proxies = {
  "http": "172.17.91.7:3128",
}

IP = raw_input("address ip:")

def check(IP):
    url = "http://www.ip138.com/ips138.asp?ip=%s&action=2"  % str(IP)
    response = requests.get(url, proxies = proxies)
    response.encoding = 'gbk'
    res = response.text
    regex = re.compile('<ul class="ul1"><li>(.*?)</li><li>(.*?)</li><li>(.*?)</li></ul>')
    data = regex.findall(res)[0]
    print(data[0])
    print(data[1])
    print(data[2])

check(IP)
