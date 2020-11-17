#!/usr/bin/env python

#冒泡排序法

l=[3,1,4,6,8,13,7,14,9,25,17,22,30,25,14,9,25,17,22,30,25,27,39]

for j in range(1,len(l)):
    for i in range(len(l)-j):
        if l[i] > l[i+1]:
            l[i],l[i+1] = l[i+1],l[i]


print l
