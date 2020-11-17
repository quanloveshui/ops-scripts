#!/usr/bin/env python

#二分查找法

def f(l,m):
     if len(l)>=1:
         n=len(l)/2
         if l[n] > m:
             return f(l[:n],m)
         elif l[n] < m:
             return f(l[n:],m)
         else:
             print 'find %s' % l[n]
     else:
         print  'not find'




l=list(range(1000))

f(l,3)
