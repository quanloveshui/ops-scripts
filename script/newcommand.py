#!/usr/bin/env python

#python批量在多台服务器上执行命令

import paramiko
import sys
 
class SSHParamiko(object):
 
    err = "argument passwd or rsafile can not be None"
 
    def __init__(self, host, port, user, rsafile=None):
        self.h = host
        self.p = port
        self.u = user
        self.rsa = rsafile
 
    def _connect(self):
        if self.rsa:
            return self.rsa_connect()
        else:
            raise ConnectionError(self.err)
 
    def _transfer(self):
        if self.rsa:
            return self.rsa_transfer()
        else:
            raise ConnectionError(self.err)
 
    def rsa_connect(self):
        pkey = paramiko.RSAKey.from_private_key_file(self.rsa)
        conn = paramiko.SSHClient()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn.connect(hostname=self.h, port=self.p, username=self.u, pkey=pkey)
        return conn
 

    def rsa_transfer(self):
        pkey = paramiko.RSAKey.from_private_key_file(self.rsa)
        transport = paramiko.Transport(self.h, self.p)
        transport.connect(username=self.u, pkey=pkey)
        sftp = paramiko.SFTPClient.from_transport(transport)
        return sftp, transport
 
    def run_cmd(self, cmd):
        conn = self._connect()
        stdin, stdout, stderr = conn.exec_command(cmd)
        code = stdout.channel.recv_exit_status()
        stdout, stderr = stdout.read(), stderr.read()
        conn.close()
        if not stderr:
            print(self.color_str("{} execute detail:".format(self.h), "yellow"))
            info = f"{cmd} | code => {code}\nResult:\n{stdout.decode()}"
            print(self.color_str(info,'green')) 
            return code, stdout.decode()
        else:
            print(self.color_str("{} execute detail:".format(self.h), "yellow"))
            info = f"{cmd} | code => {code}\nResult:\n{stdout.decode()}"
            print(self.color_str(info,'red'))
            return code, stderr.decode()
 
    def get_file(self, remote, local):
        sftp, conn = self._transfer()
        sftp.get(remote, local)
        conn.close()
 
    def put_file(self, local, remote):
        sftp, conn = self._transfer()
        sftp.put(local, remote)
        conn.close()


    
    @staticmethod
    def color_str(old, color=None):
        """给字符串添加颜色"""
        if color == "red":
            new = "\033[31;1m{}\033[0m".format(old)
        elif color == "yellow":
            new = "\033[33;1m{}\033[0m".format(old)
        elif color == "blue":
            new = "\033[34;1m{}\033[0m".format(old)
        elif color == "green":
            new = "\033[36;1m{}\033[0m".format(old)
        else:
            new = old
        return new

        

if __name__ == '__main__':
    h = "192.168.247.130"
    p = 22
    u = "root"
    rsa = '/opt/id_rsa'
 
    obj = SSHParamiko(h, p, u, rsa)
    #r = obj.run_cmd("/opt/cnd.py")
    #r = obj.get_file("/opt/cdn.py","/tmp/cdn.py")
    cmd = sys.argv[1]
    r = obj.run_cmd(cmd)
