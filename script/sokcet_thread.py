#!/bin/env python
#python socket长连接 多线程

import socket
import sys
import time
import optparse
import datetime
import urllib
import fcntl
import os
import threading

def hls(n):
    HOST="172.17.91.130"
    PORT=13001
    BUFFSIZE=5120

    #cid=sys.argv[1]
    cid="6117099895556651277"
    p=""

    sock_timeout = 3
    socket.setdefaulttimeout(sock_timeout)

    c=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    c.connect((HOST,PORT))
#fcntl.fcntl(c,fcntl.F_SETFL,os.O_NONBLOCK)

    while 1:
        getContent= "GET /%s.m3u8?Contentid=%s&channel-id=ystenlive&livemode=1 HTTP/1.1\r\n\
Accept-Encoding: identity\r\n\
Connection: keep-alive \r\n\
Host: %s:%s\r\n\r\n" %(cid,cid,HOST,PORT)
	uri=("http://%s:%s/%s.m3u8?Contentid=%s&channel-id=ystenlive&livemode=1")%(HOST,PORT,cid,cid)
        print getContent
	c.send(getContent)
        time.sleep(0.1)
        response = c.recv(BUFFSIZE)
	file="/opt/yqh/%s.m3u8.%s" %(cid,n)
	f = open(file,"w")
	beg = response.find('HTTP/1.1')
	end = response.find('\r\n\r\n',beg)
	body_m3u8 = len(response[beg:end])
        beg_1 = response.find('Content-Length:')
        end_1 = response.find('\r\n',beg_1)
        str = response[beg_1:end_1]
	m3uLen = str.split(':',1)[1]
	f.write(response)

	#statusM3u8=urllib.urlopen(uri).code
	#print '>> m3u8 is %s' %statusM3u8
	f.close()


	f=open(file)
	lines=f.readlines()
	line=lines[-1]
        time.sleep(1)
	global p
        if p != line:
	   p=line
        else:
           print "m3u8 not updated...."
           continue 
	line=line.strip('\n')
	line=line.strip('\r')
	line1=line + " HTTP/1.1"
	line2="http://%s:%s/"%(HOST,PORT)+line
	print line
	getContent1= "GET /%s\r\n\
Accept-Encoding: identity\r\n\
Connection: keep-alive \r\n\
Host: %s:%s\r\n\r\n" %(line1,HOST,PORT)
        print getContent1
	c.sendall(getContent1)
        time.sleep(0.1)
	response1 = c.recv(BUFFSIZE)
        beg1 = response1.find('HTTP/1.1')
        end1 = response1.find('\r\n\r\n',beg1)
        body_ts = len(response[beg1:end1])
        #print body_ts
	beg_2 = response1.find('Content-Length:')
	end_2 = response1.find('\r\n',beg_2)
	str1 = response1[beg_2:end_2]
	tsLen = str1.split(':',1)[1]
	#print tsLen
	totalLen1 = int(tsLen) + body_ts + 4
	#print totalLen1
        size = len(response1)
	while 1:
		buff = c.recv(BUFFSIZE)
                size = size + len(buff)
                #print totalLen1
                #print size
		if size < totalLen1:
			pass
		else:
			break
	statusTs=urllib.urlopen(line2).code
	print '>> TS is %s'%statusTs
	line=f.readline()
	time.sleep(1)
		
	f.close()



def fun(n):
    threads = []
    for i in range(0,n):
        t = threading.Thread(target=hls,args=(str(i),))
        threads.append(t)
    return threads


if __name__ == '__main__':
    n = int(sys.argv[1])
    for t in fun(n):
        t.setDaemon(True)
        t.start()
    #t.join()
    while 1:
        pass
