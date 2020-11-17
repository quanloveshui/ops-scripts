import requests
import json

#zabbix api使用，通过类实现

class Zabbix:
    def __init__(self, url, header, username, password):
        self.url = url
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
        return json.loads(group.content)["result"]

     #取单个主机组下所有的主机ID
    def getHostip(self,gid):
        data = {"jsonrpc": "2.0",
                "method": "host.get",
                "params": {
                    "output":["hostid","name"],
                    "groupids": gid,
                },
                "id": 1,
                "auth": self.getToken()
                }
        ips = requests.post(url=self.url, headers=self.header, data=json.dumps(data))
        return json.loads(ips.content)["result"]

    #获取单个主机下所有的监控项ID
    def getItemid(self):
        data = {"jsonrpc": "2.0",
                "method": "item.get",
                "params": {
                    "output":["itemids","key_"],
                    "hostids": 27351,
                },
                "id": 1,
                "auth": self.getToken()
                }
        ids = requests.post(url=self.url, headers=self.header, data=json.dumps(data))
        return json.loads(ids.content)["result"]
    #获取单个监控项的历史数据
    def getHistorydata(self):
        data = {"jsonrpc": "2.0",
                "method": "history.get",
                "params": {
                    "output": "extend",
                    "history": 3,
                    "itemids": 2448914,
                    "sortfield": "clock",
                    "sortorder": "DESC",
                    "limit": 1
                },
                "id": 1,
                "auth": self.getToken()
                }
        datas = requests.post(url=self.url, headers=self.header, data=json.dumps(data))
        return json.loads(datas.content)["result"]


url = "http://xxxx:xx/zabbix/api_jsonrpc.php"
header = {"Content-Type": "application/json-rpc"}
l = [{'groupid': '282', 'name': '世界杯扩容CDN-云桥'}]
test = Zabbix(url=url, header=header, username="xxx", password="xxx")
# a=test.getItemid()
# print(a)
# print(test.getHistorydata())
for i in l:
    gid = i["groupid"]
    print(test.getHostip(gid))

# items=(test.getItemid())
# for i in items:
#     itemid = i["itemid"]
#     print(test.getHistorydata(itemid))
