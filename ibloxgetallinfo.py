#!/usr/bin/env python

import os
import re
import json
import sys
sys.path.append("../tools")
from decorators import *

##==== MODEL ==========
## constants:
URL = "https://ipam.unc.edu/wapi/v2.10.1"
USR = 'admin'
PWD = 'ibIPAM2017'
search_patt = "record:{}?name~={}&view=network"

# defaults:
MODE = 'GET'

## parameters:
parms = {'url':URL}
parms['usr'] = USR
parms['pwd'] = PWD
parms['mode'] = MODE
parms['_paging'] = 1
parms['_max_results'] = 1000
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
def getinfo(node, ntype):
	"""return the host from an IP address"""
	global search_patt
	search = search_patt.format(ntype, node)
	if DEBUG: print("in 'getinfo().....")
	if DEBUG: print('search is:')
	print(search)
	if DEBUG: print
	ans = json.loads(getdata(search))
	if DEBUG: print('ans is: ')
	if DEBUG: print(type(ans))
	if DEBUG: print(ans)
	if DEBUG: print(len(ans))
	if len(ans) == 0 :
		print("no associted records found")
	return ans

@myprofilefunc
def main(node, ntype):
	"""return the result of the object request"""
	if DEBUG: print("in 'main.....")
	return getinfo(node, ntype)

###===== VIEW ===============
if __name__ == '__main__':
	"""run the code"""	
	supported = setsupportedobjs()
	
	try:
		if sys.argv[1] !=[]:
			node, ntype  = sys.argv[1:]
		else:
			raise IndexError
	except IndexError:
		node, ntype = raw_input("what node, type?(node|class): ").split(",")
		
	node = node.strip()
	ntype = ntype.strip()	
	print("the results for: '{}' '{}'\n".format(node, ntype))
	search = search_patt.format(ntype, node)
	ans = main(node, ntype)
	if DEBUG: print("\n\nI'm back from the functions now...")
	if DEBUG: print(type(ans))
	print("ans:")
	if type(ans) == type([]):
		for each in ans:
			for key,val in each.items():
				print("{}: {}".format(key,val))
			print
		print("{} items found.".format(len(ans)))
	else:
		print(ans)
	

