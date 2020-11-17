#!/usr/bin/expect -f

#expect交互式实现输入密码

set timeout  5
set host  [lrange $argv 0 0]
set name quyang
set password 1qazXDR%

spawn  ssh $host -l $name
expect {
    "(yes/no)?" {
        send "yes\r"
        expect "password:"
        send "$password\r"
    }
        "password:" {
        send "$password\r"
    }

 }

expect "quyang*"
send "sudo su -\r"
expect "password for quyang:"
send "$password\r"
expect "root*"
send "shutdown -h +1\r"
#expect "The system is going down*"
send "exit\r"
send "exit\r"
expect eof
