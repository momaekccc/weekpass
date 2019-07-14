#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-05-29 20:13:27
# @Author  : crhua 

import sys
import socket
from threading import Thread
from queue import Queue
from optparse import OptionParser

q = Queue()

#探测zookeeper未授权访问
"""

stat：列出关于性能和连接的客户端的统计信息。
echo stat |ncat 127.0.0.1 2181

ruok：测试服务器是否运行在非错误状态。
echo ruok |ncat 127.0.0.1 2181

reqs：列出未完成的请求。
echo reqs |ncat 127.0.0.1 2181

envi：打印有关服务环境的详细信息。
echo envi |ncat 127.0.0.1 2181

dump：列出未完成的会话和临时节点。
echo dump |ncat 127.0.0.1 2181
"""

def brute(ip,port):
	try:
		socket.setdefaulttimeout(5)
		sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		sock.connect((ip,int(port)))
		flag = b"envi"
		sock.send(flag)
		data = sock.recv(1024)
		# print(data)
		sock.close()
		if b'Environment' in data:
			print("{0}:{1} --- 存在zookeeper未授权访问".format(ip,port))
	except Exception as e:
		# print(e)
		pass

#将文件ip加入队列
def put_queue(file):
	with open(file,'r') as f:
		ips = f.readlines()
	for i in ips:
		i = i.strip()
		q.put(i)
	f.close()

#探测多个ip
def run(port):
	while not q.empty():
		ip = q.get()
		brute(ip, port)

#扫描开放zookeeper端口的ip
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
	parser.add_option("-p", dest="port", default="2181", help="target port")
	parser.add_option("-a", dest="hosts" , help="target hosts file")
	options,args = parser.parse_args()

	"""
	获取自定义端口
	"""

	if options.port:
		port = options.port

	"""
	tmp_list 存放所有文件内的ip
	last_list 存放只开放zookeeper的ip
	"""
	tmp_list = []
	last_list = []

	if options.host:
		host = options.host
		# print(host)
		brute(host, port)
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
		file_name = "{0}_zookeeper.txt".format(port)
		for i in range(10):
			threads = [Thread(target=scan,args=(u,port,file_name,)) for u in tmp_list]
		for t in threads:
			t.start()
		for t in threads:
			t.join()

		"""
		探测zookeeper未授权访问
		"""
		put_queue(file_name)
		run(port)
	else:
		print("Please use -h param")




