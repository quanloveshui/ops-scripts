#!/usr/bin/env python
# coding=utf-8
#python统计redis的key

import redis

pool1 = redis.ConnectionPool(host='x.x.x.x',port=10002,db=0)  
r1 = redis.StrictRedis(connection_pool=pool1)  
keys1 = r1.keys('xcmfile.db_*')  

pool2 = redis.ConnectionPool(host='x.x.x.x',port=10003,db=0)
r2 = redis.StrictRedis(connection_pool=pool2)
keys2 = r2.keys('xcmfile.db_*') 

pool3 = redis.ConnectionPool(host='x.x.x.x',port=10004,db=0)
r3 = redis.StrictRedis(connection_pool=pool3)
keys3 = r3.keys('xcmfile.db_*')   

pool4 = redis.ConnectionPool(host='x.x.x.x',port=10001,db=0)
r4 = redis.StrictRedis(connection_pool=pool4)
keys4 = r4.keys('xcmfile.db_*')

pool5 = redis.ConnectionPool(host='x.x.x.x',port=10002,db=0)
r5 = redis.StrictRedis(connection_pool=pool5)
keys5 = r5.keys('xcmfile.db_*')

pool6 = redis.ConnectionPool(host='x.x.x.x',port=10003,db=0)
r6 = redis.StrictRedis(connection_pool=pool6)
keys6 = r6.keys('xcmfile.db_*')

#tp = type(keys) 
#print keys1 
print "73 10002 is  " + str(len(keys1)) 
print "73 10003 is  " + str(len(keys2))
print "73 10004 is  " + str(len(keys3))
print "18 10001 is  " + str(len(keys4))
print "18 10002 is  " + str(len(keys5))
print "18 10003 is  " + str(len(keys6))
