#!/usr/bin/env python
from configparser import SafeConfigParser

class TVVConfigApi(SafeConfigParser):
    def __init__(self):
        SafeConfigParser.__init__(self)
        initFile = open('/Users/rhaasnoot/Documents/workspace/tvvmiaenterprise/config.ini', 'r')
        self.read_file(initFile, None)
#        self.read(['config.ini', '../config.ini', '../../config.ini', '../../../config.ini'])
        sections = self.sections()
        #print("(sections>=<{}>".format(sections) )

class TVVConfigApp(TVVConfigApi):
    def __init__(self):
        TVVConfigApi.__init__()

# Read config.ini and store into variables

#HOST = api_config.get('app', 'HOST')
#PORT = int(api_config.get('app', 'PORT'))
#DEBUG = api_config.get('app', 'DEBUG')
#DBTYPE = api_config.get('database', 'DBTYPE')
#DBHOST = api_config.get('database', 'DBHOST')
#DBNAME = api_config.get('database', 'DBNAME')
#DBUSER = api_config.get('database', 'DBUSER')
#DBPASS = api_config.get('database', 'DBPASS')
