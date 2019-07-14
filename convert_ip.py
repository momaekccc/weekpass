#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-05-29 20:01:29
# @Author  : crhua


import sys
from IPy import IP

def getip(ips,f):
	tmp_ip = IP(ips)
	for i in tmp_ip:
		i = str(i) + "\n"
		f.write(i)


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("[*]Usage: python convert_ip.py 1.1.1.0/24")
	else:
		ips = sys.argv[1]
		# print(ips)
		with open('ips.txt','a+') as f:
			getip(ips, f)
		f.close()
		print("[+]generate success!")




