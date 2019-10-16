#!/usr/bin/env python
"""
uses Infoblox WAPI calls to retrieve information based on supported record types:
     
"""
import os
import sys
import re
import json
import requests
sys.path.append("../tools")
from decorators import *
from ibloxmodel import *	# imports URL, USR, PWD, DEFPATT, DEFMODE

global supported 

##========= CONTROL ========
@myprofilefunc
def render(lst):
	"""print the list"""
	print("".join(str(lne) for lne in ans))
	return

@myprofilefunc
def getdata(search, mode = DEFMODE):
	""" use Infoblox WALP call to return 'search' query results:
		command:		request.get("https://152.19.255.106/wapi/v2.10/%(obj)s")
		search example: "record:a?name~=.net.unc.edu&view~=External"	
	"""
	global parms
	
	session = requests.Session()
    requests.packages.urllib3.disable_warnings()
	
	if DEBUG: print("in getdata()")
	ans = None
	parms['srch'] = search
	if mode != MODE:
		parms['mode'] = mode
	#cmd = 'curl -k -u %(usr)s:%(pwd)s -X %(mode)s %(url)s/%(srch)s' % parms
	cmd = "%(url)s/%(srch)s, auth=(%(usr)s,%(pwd)s, verifiy=false" % parms
	r = requests.get(cmd)
	ans = os.popen(cmd, 'r').read()
	return ans

@myprofilefunc
def setsupportedobjs():
	"""return Infoblox supported object schema"""
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
	"""run the code
	
	node = domain, network, record
	type = a, cname, ptr, etc.
	"""	
	global supported
	supported = setsupportedobjs()
	
	try:
		if sys.argv[1] !=[]:
			node, ntype  = sys.argv[1:]
		else:
			raise IndexError
	except IndexError:
		node, ntype = raw_input("what node, type?(node|class): ").split(",")
		
	print("the results for: '{}' '{}'\n".format(node, ntype))
	search = search_patt.format(ntype, node)
	ans = main(node, ntype)
	if DEBUG: print("\n\nI'm back from the functions now...")
	if DEBUG: print(type(ans))
	print("ans:")
	print(ans)
	

