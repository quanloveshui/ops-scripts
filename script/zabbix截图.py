import requests
import json
import datetime, time
import os
import urllib
import http.cookiejar


class Zabbix:
    def __init__(self, url,gr_url,login_url,header, username, password):
        self.url = url
        self.gr_url = gr_url
        self.login_url = login_url
        self.header = header
        self.username = username
        self.password = password

    def getToken(self):
        # 获取Token并返回字符Token字符串

        data = {"jsonrpc": "2.0",
                "method": "user.login",
                "params": {
                    "user": self.username,
                    "password": self.password
                },
                "id": 1,
                "auth": None
                }
        token = requests.post(url=self.url, headers=self.header, data=json.dumps(data))
        return json.loads(token.content)["result"]

    #获取所有主机组id
    def getHostgroup(self):
        data = {"jsonrpc": "2.0",
                "method": "hostgroup.get",
                "params": {
                    "output": ["groupid", "name"],
                },
                "id": 1,
                "auth": self.getToken()
                }
        group = requests.post(url=self.url, headers=self.header, data=json.dumps(data))
        #print(json.loads(group.content)["result"])
        return json.loads(group.content)["result"]

     #取单个主机组下所有的主机ID
    def getHostid(self,gid):
        data = {"jsonrpc": "2.0",
                "method": "host.get",
                "params": {
                    "output":["hostid","name"],
                    "groupids": gid,
                },
                "id": 1,
                "auth": self.getToken()
                }
        ids = requests.post(url=self.url, headers=self.header, data=json.dumps(data))
        return json.loads(ids.content)["result"]

    #根据ip获取主机id
    def gethostid(self,ip):
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": ["hostid","name"], #"extend"
                "filter": {
                    "host": ip
                }
            },
            "auth": self.getToken(),
            "id": 1
                }
        hostid = requests.post(url=self.url, headers=self.header, data=json.dumps(data))
        return json.loads(hostid.content)["result"]


    #根据hostid获取graphid
    def getgraphid(self,hostid):
        data = {
            "jsonrpc": "2.0",
            "method": "graph.get",
            "params": {
                "output": "name",
                "hostids": hostid,
                "sortfield": "name",
                "filter": {
                    "name": ['gsd调度次数','gsd平均调度时间']
                }
            },
            "auth": self.getToken(),
            "id": 1
        }
        graps = requests.post(url=self.url, headers=self.header, data=json.dumps(data))
        return json.loads(graps.content)["result"]

    #下载保存图片
    def get_graph(self,starttime,dirs,graphid,graphname):
        login_data = urllib.parse.urlencode({
            "name": self.username,
            "password": self.password,
            "autologin": 1,
            "enter": "Sign in"}).encode(encoding='UTF8')

        graph_args = urllib.parse.urlencode({
            "graphid": graphid,
            "width": '1200',
            "height": '156',
            "stime": starttime,  # 图形开始时间
            "period": '86400'}).encode(encoding='UTF8')
        cj = http.cookiejar.CookieJar()  # 设置一个cookie处理器, 它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        urllib.request.install_opener(opener)
        opener.open(login_url, login_data).read()
        data = opener.open(gr_url, graph_args).read()
        if os.path.exists(dirs):
            pass
        else:
            os.makedirs(dirs)
        with open(r"%s//%s-%s.png" % (dirs,graphname, datetime.datetime.now().strftime('%Y%m%d')), 'wb') as f:
            f.write(data)




if __name__ == "__main__":
    url = "http://x.x.x.x/zabbix/api_jsonrpc.php"
    #获取图片url
    gr_url = "http://x.x.x.x/zabbix/chart2.php"
    #登录url
    login_url = 'http://x.x.x.x:18080/zabbix/index.php'
    #header 头
    header = {"Content-Type": "application/json-rpc"}

    #获取当天零点
    #now = datetime.datetime.now()
    #zeroToday = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,microseconds=now.microsecond)

    # 图形开始时间
    starttime = int(time.mktime((datetime.datetime.now() - datetime.timedelta(days=1)).timetuple()))
    #starttime = int(time.mktime((zeroToday - datetime.timedelta(days=0)).timetuple()))

    #图片保存路径
    dirs = r"D://PyChram-progect//zabbix//%s" % (datetime.datetime.now().strftime('%Y%m%d'))


    test = Zabbix(url=url,gr_url=gr_url,login_url=login_url, header=header, username="xx", password="xx")
    #ziyan_group=test.getHostgroup()[-1]
    #ziyan_host=test.getHostid(ziyan_group['groupid'])

    hostid = test.gethostid('10.200.207.106')
    hostid = hostid[0]['hostid']
    #print(hostid)
    graps = test.getgraphid(hostid)
    #print(graps)
    for i in graps:
        print('%s的截图 已经成功保存至%20s' % (i['name'],dirs.replace('//','\\')))
        test.get_graph(starttime,dirs,i['graphid'],i['name'])




