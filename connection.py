#!/usr/bin/env python

import pyzabbix as zb
import redis
import sys
from pyzabbix import ZabbixAPIException
from requests import Session, exceptions
from zabexceptions import *

# if any is true, I know that 'check_output' is at least present and I can manually start redis-server
try:
	import subprocess
	if not any([ 'check_output' in subprocess.__dict__.keys(),
		subprocess.check_output(['pidof', 'redis-server'] is not None)]):
		raise InvalidModule("Invalid Module Subprocess:  No 'check_output' method\n")
	print "Attempting to start redis-server"
	cmds = ['redis-server', '--port 10000', '--daemonize yes']
	redisstart = subprocess.Popen(cmds).communicate()
	if not subprocess.check_output (['pidof', 'redis-server']):
		sys.exit("Failed to Start Redis-Server")
except InvalidModule:
	print "Failed to Load Subprocess"


class CredentialStore(object):
	"""
	Decided not to instantiate redis connection.  This is to avoid conflict with port 10000
	"""
	def redisConnection(self):
		self.conn = redis.Redis('localhost', 10000)
		
	def keystore(self):
		return {
			'password': 'passwd',
			'username': 'usern',
			'secretkeys': 'secret'
		}
		
	def storeCredentials(self, memvalue, storetype):
		if not isinstance(memvalue, (dict, list)):
			print "Invalid Memory Cache Type: {}".format(
				type(memvalue)
			)
		j = self.keystore()
		self.conn.hmset(
			j.get(storetype), memvalue
		)


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
			self.timeout = 25
		except (exceptions.ConnectionError, ZabbixConnection, ZabbixAPIException):
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
