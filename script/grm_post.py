#!/usr/bin/env python
import urllib
import urllib2
import time

url = 'http://x.x.x.x:x'
file = open('grm.xml')
content = file.read()
file.close()
print content
req = urllib2.Request(url,content)
response = urllib2.urlopen(req)
message = response.read()
print message


文件grm.xml里内容如下：
<?xml version="1.0" encoding="UTF-8" ?>
<message module="CDN" version="3.0">
<header action="REQUEST" command="COMPONENT_ADD" component-id="XRM01" component-type="WEB" sequence="100000001"/>
 <body>
  <pop id="GanSu-RongHe-CDN" description="GanSu-RongHe-CDN">
    <component id="GanSu-RongHe-CDN" logic-id="GanSu-RongHe-CDN" version="1.1.1.1" type="XSD"  description="" device-id="ddh" health-status="1"                       service-status="1" control-ip="1.1.1.1"
      control-port="6180" command-ip="1.1.1.1" command-port="6010"  
       monitor-ip="1.1.1.1" monitor-port="161"
       log-ftp-user="123" log-ftp-password="123"
       provider="SiHua">
       <capability concurrencies="50000" bandwidth="1000000" disk-writing-speed="1000">
       </capability>
         <services> 
               <service protocol="HTTP" ip="xxx" port="80" />  
              <service protocol="IPHONEHTTP" ip="xxx" port="80" />   
            </services>                                  
  </component>
            </pop>
         </body>
</message>
