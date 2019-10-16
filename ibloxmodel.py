##==== MODEL ==========
## constants:
APIURL = "https://ipam.unc.edu/wapi/v2.10.1"
USR = 'admin'
PWD = 'ibIPAM2017'
DEFPATT = "{}:{}?{}&view={}"  # (obj, typ, qry, view)
DEFMODE = 'GET'		# [GET|PUT|POST|DELETE]
DEFOBJ = ''
VIEW = 'External'
## parameters:
DEFPARMS = {'url':APIURL}
DEFPARMS['usr'] = USR
DEFPARMS['pwd'] = PWD

REQPARMS = {
'zone':'unc.edu',
'view':VIEW,
}

## debug
DEBUG = 0

