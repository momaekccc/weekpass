#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-05-29 20:13:27
# @Author  : crhua 

import sys
import pymongo
import socket
from threading import Thread
from optparse import OptionParser


"""
brute mongodb login
"""

def brute(ip,port):
	try:
		client_one = pymongo.MongoClient(ip,int(port))
		db_one = client_one.database_names()
		if db_one:
			res = "[+] success: {0}:{1} ---- 存在mongodb未授权访问".format(ip,port)
			# print(res)
			result.append(res)
			return res
	except Exception as e:
		# print(e)
		pass


"""
多个目标
"""
def run(func,threadnum,ips,port):
	for i in range(1,threadnum + 1):
		threads = [Thread(target=func,args=(u,port,)) for u in ips]
	for t in threads:
		t.start()
	for t in threads:
		t.join()



"""
扫描开放端口
"""
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
	parser.add_option("-p", dest="port", default="27017", help="target port")
	parser.add_option("-a", dest="hosts" , help="target hosts file")
	options,args = parser.parse_args()

	"""
	获取用户参数 -p
	"""
	if options.port:
		port = options.port

	"""
	tmp_list 存放所有文件内的ip
	last_list 存放只开放mongodb的ip
	result 结果存放列表
	threadnum 多线程数量
	"""
	tmp_list = []
	last_list = []
	result = []
	threadnum = 10

	if options.host:
		host = options.host
		brute(host,port)
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
		file_name = "{0}_mongo.txt".format(port)
		for i in range(10):
			threads = [Thread(target=scan,args=(u,port,file_name,)) for u in tmp_list]
		for t in threads:
			t.start()
		for t in threads:
			t.join()
		print(file_name)

		"""
		暴力破解mongodb
		"""
		with open(file_name,'r') as f:
			_last = f.readlines()
		for i in _last:
			i = i.strip()
			last_list.append(i)
		run(brute,threadnum,last_list,port)
	else:
		print("Error! Please use -h param")

	for m in result:
		print(m)


		

