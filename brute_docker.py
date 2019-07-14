#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-05-29 20:13:27
# @Author  : crhua 

import sys
import requests
import socket
from threading import Thread
from optparse import OptionParser


"""
docker api 未授权访问
端口2375 2376
"""
def brute(ip,port):
	try:
		url_path = '/containers/json?all=1'
		url = 'http://{0}:{1}/{2}'.format(ip,port,url_path)
		res = requests.get(url,timeout=5)
		rcode = res.status_code
		if rcode == 200:
			_t = "[+] success: {0}:{1} 存在docker api 未授权访问漏洞".format(ip,port)
			result.append(_t)
	except Exception as e:
		# print(e)
		pass

"""
多个目标
"""
def run(func,threadnum,ips,port):
	for i in range(1,threadnum + 1):
		threads = [Thread(target=func,args=(u,port)) for u in ips]
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
	parser.add_option("-p", dest="port", default="2375", help="target port")
	parser.add_option("-a", dest="hosts" , help="target hosts file")
	options,args = parser.parse_args()

	"""
	获取用户参数 -u -P -p
	"""
	if options.port:
		port = options.port

	"""
	tmp_list 存放所有文件内的ip
	last_list 存放只开放docker的ip
	result 结果存放列表
	threadnum 多线程数量
	"""
	tmp_list = []
	last_list = []
	result = []
	threadnum = 50


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
		file_name = "{0}_docker.txt".format(port)
		for i in range(20):
			threads = [Thread(target=scan,args=(u,port,file_name,)) for u in tmp_list]
		for t in threads:
			t.start()
		for t in threads:
			t.join()
		print(file_name)

		"""
		批量探测docker api 未授权访问漏洞
		"""
		with open(file_name,'r') as f:
			_last = f.readlines()
		for i in _last:
			i = i.strip()
			last_list.append(i)
		run(brute,threadnum,last_list,port)
	else:
		print("Please use -h param")

	for m in result:
		print(m)


		

