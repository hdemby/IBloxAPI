#!/usr/bin/env python

import os
import sys
import re
import json
import requests
sys.path.append("../tools")
from decorators import myprofilefunc

global supported

##==== MODEL ==========
## constants:
URL = "https://ib-ipam-test.net.unc.edu/wapi/v2.10"
USR = 'admin'
PWD = 'ibIPAM2017'
search_patt = "network/{}/{}&network_view=network"
inputs = ['network', 'cidr']

# defaults:
MODE = 'GET'
DEBUG = 1

## parameters:
parms = {'apiurl':URL}
parms['usr'] = USR
parms['pwd'] = PWD
parms['mode'] = MODE
perms['view'] = 'network'


def getdata(parms, mode = MODE):
	""" use 'curl' call to return 'obj' query results
	infoblox API get command:$(apiurl)s/%(obj)s?%(srch)s
	obj example:  record:a?name~=.net.unc.edu&view~=External"
	
	"""
	
	if DEBUG: print("in getdata()")
	ans = None
	if mode != MODE:
		parms['mode'] = mode
	cmd = r'%(apiurl)s/%(obj)s auth=(%usr)s,%(pwd)s) data=%(srch)s view=%(view)s' % parms
	cmd = requests.get(cmd)
	ans = os.popen(cmd, 'r').read()
	return ans
	
def setsupportedobjs():
	"""return Infoblox supported objects
	result from:
	curl -k1 -u admin:ibIPAM2017 -X GET https://152.19.255.106/wapi/v2.10/?_schema&_return_as_object=1
	
	"""
	global parms
	global supported
	
	parms['obj'] = "?_schema&_return_as_object=1"
	parms['srch'] = None
	supported = eval(getdata(parms))['supported_objects']
	return supported

## from ibloxWAPItests import *
## [itm for itm in supported if re.compile('^record').match(itm)]
## cmd_patt = 'curl -k -u %(usr)s:%(pwd)s -X %(mode)s %(url)s/%(srch)s' % parms
## url = "curl -k1 -u admin:ibIPAM2017 -X GET https://152.19.255.106/wapi/v2.10/"
## srch_info = "record:a?name~=\.net.unc.edu&network_view=default"
## srch = url + srch_info
## >>> search = 'curl -k -u %(usr)s:%(pwd)s -X %(mode)s %(url)s/range&view=default' % parms
## ans = getdata(search)
