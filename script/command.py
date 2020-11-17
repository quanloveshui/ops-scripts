#!/usr/bin/env python

#python批量在多台服务器上执行命令

import paramiko
import sys
 
class SSHParamiko(object):
 
    err = "argument passwd or rsafile can not be None"
 
    def __init__(self, host, port, user, passwd=None, rsafile=None):
        self.h = host
        self.p = port
        self.u = user
        self.w = passwd
        self.rsa = rsafile
 
    def _connect(self):
        if self.w:
            return self.pwd_connect()
        elif self.rsa:
            return self.rsa_connect()
        else:
            raise ConnectionError(self.err)
 
    def _transfer(self):
        if self.w:
            return self.pwd_transfer()
        elif self.rsa:
            return self.rsa_transfer()
        else:
            raise ConnectionError(self.err)
 
    def pwd_connect(self):
        conn = paramiko.SSHClient()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn.connect(self.h, self.p, self.u, self.w)
        return conn
 
 
    def pwd_transfer(self):
        transport = paramiko.Transport(self.h, self.p)
        transport.connect(username=self.u, password=self.w)
        sftp = paramiko.SFTPClient.from_transport(transport)
        return sftp, transport
 
 
    def run_cmd(self, cmd):
        conn = self._connect()
        stdin, stdout, stderr = conn.exec_command(cmd)
        code = stdout.channel.recv_exit_status()
        stdout, stderr = stdout.read(), stderr.read()
        conn.close()
        if not stderr:
            return code, stdout.decode()
        else:
            return code, stderr.decode()
 
    def get_file(self, remote, local):
        sftp, conn = self._transfer()
        sftp.get(remote, local)
        conn.close()
 
    def put_file(self, local, remote):
        sftp, conn = self._transfer()
        sftp.put(local, remote)
        conn.close()

if __name__ == '__main__':
    h = "192.168.149.129"
    p = 22
    u = "root"
    w = "1qazXDR%"
 
    obj = SSHParamiko(h, p, u, w)
    #r = obj.run_cmd("/opt/cnd.py")
    #r = obj.get_file("/opt/cdn.py","/tmp/cdn.py")
    cmd = sys.argv[1]
    r = obj.run_cmd(cmd)
    print(r[0])
    print(r[1])
