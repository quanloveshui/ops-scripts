#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'young'

#核心类
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
import json

class ModelResultsCollector(CallbackBase):
    """
    重写callbackBase类的部分方法
    """
    def __init__(self, *args, **kwargs):
        super(ModelResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}
    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result
    def v2_runner_on_ok(self, result):
        self.host_ok[result._host.get_name()] = result
    def v2_runner_on_failed(self, result,ignore_errors=False):
        self.host_failed[result._host.get_name()] = result


class AnsibleApi(object):
    def __init__(self):
        self.Options = namedtuple('Options',
                     ['connection',
                      'remote_user',
                      'ask_sudo_pass',
                      'verbosity',
                      'ack_pass',
                      'module_path',
                      'forks',
                      'become',
                      'become_method',
                      'become_user',
                      'check',
                      'listhosts',
                      'listtasks',
                      'listtags',
                      'syntax',
                      'sudo_user',
                      'sudo',
                      'diff'])
        self.options = self.Options(connection='smart',
                       remote_user=None,
                       ack_pass=None,
                       sudo_user=None,
                       forks=5,
                       sudo=None,
                       ask_sudo_pass=False,
                       verbosity=5,
                       module_path=None,
                       become=None,
                       become_method=None,
                       become_user=None,
                       check=False,
                       diff=False,
                       listhosts=None,
                       listtasks=None,
                       listtags=None,
                       syntax=None)

        self.loader = DataLoader()
        self.inventory = InventoryManager(loader=self.loader, sources=['/opt/myops/myansible/hosts'])
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        self.callback = ModelResultsCollector()
        self.passwords = dict()

    def runansible(self,host_list, task_list):

        play_source =  dict(
            name = "Ansible Play",
            hosts = host_list,
            gather_facts = 'no',
            tasks = task_list
        )
    
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)    
        tqm = TaskQueueManager(
           inventory=self.inventory,
           variable_manager=self.variable_manager,
           loader=self.loader,
           options=self.options,
           passwords=self.passwords,
           stdout_callback=self.callback,
           )

        result = tqm.run(play)
        result_raw = {'success':{},'failed':{},'unreachable':{}}
        for host,result in self.callback.host_ok.items():
            result_raw['success'][host] = result._result
        for host,result in self.callback.host_failed.items():
            result_raw['failed'][host] = result._result
        
        js = json.dumps(result_raw, sort_keys=False, indent=4)
        print (js)



if __name__ == "__main__":
    a = AnsibleApi()
    host_list = ['192.168.149.129']
    tasks_list = [
        dict(action=dict(module='shell', args='date')),
    ]

    a.runansible(host_list,tasks_list)
