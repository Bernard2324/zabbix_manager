
import json
from zabexceptions import *
from connection import ConnManager
from Crypto.Cipher import DES

class ZabbixMethodManager(ConnManager):
	
	def __init__(self):
		self.username = 'maurice.green'
		self.ciphertext = self.passwordManager(
			raw_input("Enter Secret Key: \n")
		)
		self.password = "".join(
			chr(x - 1) for x in map(ord, [j for j in self.ciphertext])
		).strip('WXYZ')
		super(ZabbixMethodManager, self).__init__(self.username, self.password)
		self.id = 0
		
	def do_request(self, method, params=None):
		request_json = {
			'jsonrpc': '2.0',
			'method': method,
			'params': params or {},
			'id': self.id
		}
		
		response = self.conn.sess.post(
			self.conn.url,
			data=json.dumps(request_json),
			timeout=self.conn.timeout
		)
		response.raise_for_status()
		
		if not len(response.text):
			raise ZabbixEmptyResponse("Received Empty Response!\n")
		
		try:
			response_json = json.loads (response.text)
		except ValueError:
			raise ZabbixGeneric(
				"Unable to parse json: %s" % response.text
			)
		self.id += 1
		
		if 'error' in response_json:  # some exception
			if 'data' not in response_json['error']:  # some errors don't contain 'data': workaround for ZBX-9340
				response_json['error']['data'] = "No data"
			msg = u"Error {code}: {message}, {data}".format (
				code=response_json['error']['code'],
				message=response_json['error']['message'],
				data=response_json['error']['data']
			)
			raise ZabbixGeneric(msg, response_json['error']['code'])
		
		return response_json
		
	def passwordManager(self, key):
		if not isinstance(key, str):
			key = str(key)
		try:
			encryptionObj = DES.new(key, DES.MODE_ECB)
			
			cipher = '\x84\xe9&\xd5h\x1f\xd3\x15\xba"j\xdd\xb5B-x\xe6\x8d\x00\xbcV\xd0\xb0('
			
			return encryptionObj.decrypt(cipher)
		except PasswordDecryption:
			print "Failed to Decrypt Password!  Please Enter Correct Key\n"


class CleanObject(object):
	pass
