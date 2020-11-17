
#pycurl检测各cdn节点服务质量  传输结束总时间，DNS解析时间，建立连接时间等

import pycurl
from io import BytesIO
from urllib import parse

class cdn(object):
    def __init__(self,url):
        self.buffer = BytesIO()
        self.c = pycurl.Curl()
        self.c.setopt(pycurl.URL,url)
        #self.c.setopt(pycurl.FOLLOWLOCATION, 1) #是否开启重定向
        #self.c.setopt(pycurl.MAXREDIRS, 1) #重定向最大次数
        self.c.setopt(pycurl.WRITEFUNCTION, self.body) #将返回的内容定向到回调函数body
        self.c.setopt(pycurl.WRITEHEADER,self.buffer) #将返回的HTTP HEADER定向到buffer对象

        try:
            self.c.perform() #提交内容
        except Exception as e:
            print('connection error:' + str(e))
            self.buffer.close()
            self.c.close()

    def body(self,buf):
        data = buf

    def gethead(self):
        head = self.buffer.getvalue()
        #print(head)
        self.buffer.close()
        self.c.close()
        return head

    def getinfo(self,url):
        host,port = self.url_parse(url)
        h1 = self.c.getinfo(pycurl.HTTP_CODE)  # 状态码
        h2 = self.c.getinfo(pycurl.TOTAL_TIME)  # 传输结束总消耗时间
        h3 = self.c.getinfo(pycurl.NAMELOOKUP_TIME)  # DNS解析时间
        h4 = self.c.getinfo(pycurl.CONNECT_TIME)  # 建立连接时间
        h5 = self.c.getinfo(pycurl.PRETRANSFER_TIME)  # 建立连接到准备传输消耗时间
        h6 = self.c.getinfo(pycurl.STARTTRANSFER_TIME)  # 从建立连接到传输开始消耗时间
        h7 = self.c.getinfo(pycurl.REDIRECT_TIME)  # 重定向消耗时间
        h8 = self.c.getinfo(pycurl.SIZE_UPLOAD)  # 上传数据包大小
        h9 = self.c.getinfo(pycurl.SIZE_DOWNLOAD)  # 下载数据包大小
        h10 = self.c.getinfo(pycurl.SPEED_DOWNLOAD)  # 平均下载速度
        h11 = self.c.getinfo(pycurl.SPEED_UPLOAD)  # 平均上传速度
        h12 = self.c.getinfo(pycurl.HEADER_SIZE)  # http头文件大小
        #h13 = self.c.getinfo(pycurl.EFFECTIVE_URL) #重定向url
        #h14 = self.c.getinfo(pycurl.REDIRECT_COUNT) #重定向次数
        info ='''
            请求 %s:%s 响应信息如下:
            http状态码：%s
            传输结束总时间：%.2f ms
            DNS解析时间：%.2f ms
            建立连接时间：%.2f ms
            准备传输时间：%.2f ms
            传输开始时间：%.2f ms
            重定向时间：%.2f ms
            上传数据包大小：%d bytes/s
            下载数据包大小：%d bytes/s
            平均下载速度：%d bytes/s
            平均上传速度：%d bytes/s
            http头文件大小：%d byte
        ''' %(host,port,h1,h2*1000,h3*1000,h4*1000,h5*1000,h6*1000,h7*1000,h8,h9,h10,h11,h12)
        #print(info)
        #self.buffer.close()
        #self.c.close()
        return info

    def url_parse(self,url):
         host = parse.urlparse(url).hostname
         port = parse.urlparse(url).port
         #print(port)
         return host,port

    def get_url(self):
        url = ''
        res = self.gethead()
        head = res.decode("utf-8").split("\r\n")
        for i in head:
            if 'Location' in i:
                #print(i.split()[1])
                url = i.split()[1]
        return url

if __name__ == '__main__':
    url = "http://x.x.x.x.:8080/000000001001/xxxxxx.ts?xxxx"
    #url = "http://x.x.x.x:8080/000000001001/xxxx.m3u8?cxxxxx"
    while url != '':
        respon = cdn(url)
        info = respon.getinfo(url)
        hostname = respon.url_parse(url)
        url = respon.get_url()
        print(info)
