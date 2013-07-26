#!/usr/bin/python
#coding:utf-8

'''
这个程序模拟PYJOB运行的典型流程
'''

import time

print "example for python"

print "START"
time.sleep(1)

#read cursor 
cur=2
for i in range(1, cur):
	print "HEARTBEAT"
	time.sleep(1)
#write cursor

time.sleep(1)
print "END"
