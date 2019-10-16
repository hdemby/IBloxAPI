#!/usr/bin/env python

import os
import sys
import re
import json

from decorators import *

##==== MODEL ==========
## constants:
URL = "https://ib-ipam-test.net.unc.edu/wapi/v2.10"
USR = 'admin'
PWD = 'ibIPAM2017'

# defaults:
MODE = 'GET'

## parameters:
parms = {'url':URL}
parms['usr'] = USR
parms['pwd'] = PWD
parms['mode'] = MODE
global supported 

## diagnostics
DEBUG = 0

##========= CONTROL ========
@myprofilefunc
def render(lst):
	"""print the list"""
	print("".join(str(lne) for lne in ans))
	return

@myprofilefunc
def getdata(search, mode = MODE):
	""" use 'curl' call to return 'obj' query results
	curl -k1 -u admin:ibIPAM2017 -X GET https://152.19.255.106/wapi/v2.10/
	obj example:  record:a?name~=.net.unc.edu&view~=External"
	
	"""
	global parms
	
	if DEBUG: print("in getdata()")
	ans = None
	parms['srch'] = search
	if mode != MODE:
		parms['mode'] = mode
	cmd = 'curl -k -u %(usr)s:%(pwd)s -X %(mode)s %(url)s/%(srch)s' % parms
	ans = os.popen(cmd, 'r').read()
	return ans

@myprofilefunc
def setsupportedobjs():
	"""return Infoblox supported objects
	result from:
	curl -k1 -u admin:ibIPAM2017 -X GET https://152.19.255.106/wapi/v2.10/?_schema&_return_as_object=1
	
	"""
	global parms
	global supported
	
	obj = "?_schema&_return_as_object=1"
	supported = eval(getdata(obj))['supported_objects']
	return supported

@myprofilefunc
def goodobj(srchstr):
	"""determine if search object is valid"""
	obj = search.split(':')[0]
	objpatt = re.compile(obj)
	for types in supported:
		if objpatt.search(types):
			return True
	return False
	
@myprofilefunc
def getinfo(search):
	"""return the host from an IP address"""
	if DEBUG: print("in 'getinfo().....")
	if DEBUG: print('search is:')
	if DEBUG: print(search)
	if DEBUG: print
	ans = json.loads(getdata(search))
	if DEBUG: print('ans is: ')
	if DEBUG: print(type(ans))
	if DEBUG: print(ans)
	if DEBUG: print(len(ans))
	if len(ans) == 0 :
		print("no associted ip found")
		sys.exit()
	else:
		if DEBUG: print(type(ans[0]))
		if DEBUG: print(ans[0])
		try:
			ansdict = ans[0]
		except:
			print("no IP is currently associated with '{}' in infoblox".format(fqdn))
			sys.exit()

	#print(ansdict.keys())
	#for key in ansdict.keys():
	#	print("{}: {}".format(key, ansdict[key]))
	return ansdict

@myprofilefunc
def main(srch, mode = MODE):
	"""return the result of the object request"""
	if DEBUG: print("in 'main.....")
	return getinfo(srch)

###===== VIEW ===============
if __name__ == '__main__':
	"""run the code"""	
	global supported
	supported = setsupportedobjs()
	
	try:
		if sys.argv[1] !=[]:
			fqdn = sys.argv[1]
		else:
			raise IndexError
	except IndexError:
		fqdn = raw_input("what FQDN?: ")
		
	print('Hostname FQDN is {}\n'.format(fqdn))
	#search = "ipv4address?ip_address={}&network_view=network".format(ip)
	search = "record:host?name={}&view=network".format(fqdn)
	ans = main(search)
	if DEBUG: print("\n\nI'm back from the functions now...")
	if DEBUG: print(type(ans))
	if DEBUG: print("ans:")
	if DEBUG: print(ans)
	
	if ans != None and 'ipv4addr' in ans['ipv4addrs'][0].keys():
		ip = ans['ipv4addrs'][0]['ipv4addr']
		print("host: '{}' <==> ip: '{}'".format(fqdn, ip))
	else:
		print("no IP is currently associated with {}".format(fqdn)) 


