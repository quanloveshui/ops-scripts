import requests
import json


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
    def getItemid(self,hid,filters):
        data = {"jsonrpc": "2.0",
                "method": "item.get",
                "params": {
                    "output":["itemids","key_"],
                    "hostids": hid,
                    "filter": {
                        "key_": filters
                    },
                },
                "id": 1,
                "auth": self.getToken()
                }
        ids = requests.post(url=self.url, headers=self.header, data=json.dumps(data))
        return json.loads(ids.content)["result"]
    #获取单个监控项的历史数据
    def getHistorydata(self,itemid):
        data = {"jsonrpc": "2.0",
                "method": "history.get",
                "params": {
                    "output": "extend",
                    "history": 3,
                    "itemids": itemid,
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
nginx_cluster=[{'hostid': '23827', 'name': 'x.x.x.x-x-nginx-x'},
{'hostid': '23828', 'name': 'x.x.x.x-x-nginx-x'},
{'hostid': '23829', 'name': 'x.x.x.x-x-nginx-x'},
{'hostid': '23830', 'name': 'x.x.x.x-x-nginx-x'},
{'hostid': '23831', 'name': 'x.x.x.x-x-nginx-x'},
{'hostid': '23832', 'name': 'x.x.x.x-x-nginx-x'},
{'hostid': '23833', 'name': 'x.x.x.x-x-nginx-x'},
{'hostid': '23834', 'name': 'x.x.x.x-x-nginx-x'},]
cache_cluster = [{'hostid': '23835', 'name': 'x.x.x.x-x-cache-x-x'},
{'hostid': '23836', 'name': 'x.x.x.x-x-cache-x-x'},
{'hostid': '23837', 'name': 'x.x.x.x-x-cache-x-x'},
{'hostid': '23838', 'name': 'x.x.x.x-x-cache-x-x'},
{'hostid': '23839', 'name': 'x.x.x.x-x-cache-x-x'},
{'hostid': '23840', 'name': 'x.x.x.x-x-cache-x-x'},
{'hostid': '23841', 'name': 'x.x.x.x-x-cache-x-x'},
{'hostid': '23842', 'name': 'x.x.x.x-x-cache-x-x'},
]

def getvalue(host):
    filters_list = ['net.if.out[bond0]','net.if.in[bond0]']
    data_total = {}
    data_detail= {}
    for filters in filters_list:
        total = 0
        singles = {}
        for h in host:
            hid = h["hostid"]
            name = h["name"]
            items = test.getItemid(hid,filters)
            itemid = items[0]["itemid"]
            value = test.getHistorydata(itemid)[0]["value"]
            singles[name]=int(value)/1000000000
            total += int(value)
        data_total[filters] = total/1000000000
        data_detail[filters]=singles

    return data_total ,data_detail

nginx=getvalue(nginx_cluster)
print(nginx)

