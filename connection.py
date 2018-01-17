#!/usr/bin/env python

import pyzabbix as zb
from requests import Session
from zabexceptions import *


class ConnectionStart(zb.ZabbixAPI):
	
	def __init__(self, host='https://swzabbix.usa.systewmare.com'):
		try:
			self.sess = Session()
			self.sess.headers.update({
				'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
				(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
			})
			setattr(getattr(self, 'sess'), 'verify', False)
			super(ConnectionStart, self).__init__(server=host, session=self.sess)
			# Once we instantiate the ZabbixAPI, we can modify self.url
			self.url = host + 'zabbix/api_jsonrpc.php'
			self.timeout = None
		except (ZabbixConnection, StandardError):
			print "Failed to Connect To Host!\n"
	

class ConnManager(object):
	
	def __init__(self, u, p):
		self.conn = ConnectionStart()
		self.conn.login(user=u, password=p)
	
	def close(self):
		if not hasattr(self, 'conn'):
			raise ZabbixConnAttribute("Failed to Locate Connection, it likely timed out!")
		# kill the existing session - calls requests.close()
		self.conn.sess.close()
		

class CleanObj(object):
	pass
