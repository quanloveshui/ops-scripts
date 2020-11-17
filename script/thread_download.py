#!/usr/bin/env python

import requests
import threading

class downloader:
    def __init__(self):
        self.url = "http://x.x.x.x:80/000000000000/5002482315/xxxx.ts?channel-id=xxxxx"
        self.num = 10
        self.name = "test.ts"
        r = requests.head(self.url)
        # 获取文件大小
        self.total = int(r.headers['Content-Length'])
        print (self.total)

    # 获取每个线程下载的区间
    def get_range(self):
        ranges = []
        offset = int(self.total/self.num)
        for i in range(self.num):
            if i == self.num-1:
                ranges.append((i*offset,''))
            else:
                ranges.append((i*offset,(i+1)*offset))
        return ranges  # [(0,100),(100,200),(200,"")]

    # 通过传入开始和结束位置来下载文件
    def download(self,start,end):
        headers = {'Range':'Bytes=%s-%s'%(start,end),'Accept-Encoding':'*'}
        res = requests.get(self.url,headers=headers)
        print ("%s-%s download success"%(start,end))
        # 将文件指针移动到传入区间开始的位置
        self.fd.seek(start)
        self.fd.write(res.content)

    def run(self):
        self.fd = open(self.name,"wb")

        thread_list = []
        n = 0

        for ran in self.get_range():
            # 获取每个线程下载的数据块
            start,end = ran
            n += 1
            thread = threading.Thread(target=self.download,args=(start,end))
            thread.start()
            thread_list.append(thread)

        for i in thread_list:
            # 设置等待，避免上一个数据块还没写入，下一数据块对文件seek，会报错
            i.join()

        self.fd.close()

if __name__ == "__main__":
    downloader().run()
