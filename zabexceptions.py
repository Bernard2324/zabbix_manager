
class ZabbixConnection(Exception):
	"""
		call this on present issues related to the zabbix connection
	"""
	pass


class ZabbixConnAttribute(Exception):
	"""
		call this if connection is called, but no connection exists
	"""
	pass


class PasswordDecryption(Exception):
	pass


class ZabbixEmptyResponse(Exception):
	pass

class ZabbixGeneric(Exception):
	pass


