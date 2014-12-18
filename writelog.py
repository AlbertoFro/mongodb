'''
#-------------------------------------------------------------------------------
# Name:        writelog mongodb
# Purpose:
#
# Author:      alberto.frosi
#
# Created:     16/12/2014
# Copyright:   (c) alberto.frosi 2014
# Licence:    Use of this source code is governed by a BSD-style
#-------------------------------------------------------------------------------
#!/usr/bin/env python
'''
import re
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT
from pymongo import Connection
from pymongo.errors import CollectionInvalid
import pymongo

HOST = 'OEL65'
LOG_PATH = '/home/oracle/jasperreports-server-cp-5.6.0/apache-tomcat/logs/localhost_access_log.2014-10-07.txt'
DB_NAME = 'mydb'
COLLECTION_NAME = 'jasper2'
MAX_COLLECTION_SIZE = 5 # in megabytes

def main():
    # connect to mongodb

    mongo_conn = Connection()
    mongo_db = mongo_conn[DB_NAME]
    try:
        mongo_coll = mongo_db.create_collection(COLLECTION_NAME,
                                                capped=True,
                                                size=MAX_COLLECTION_SIZE*1048576)
    except CollectionInvalid:
        mongo_coll = mongo_db[COLLECTION_NAME]

    # open remote log file
    cmd = 'tail -f /home/oracle/jasperreports-server-cp-5.6.0/apache-tomcat/logs/localhost_access_log.2014-10-07.txt'
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
    # parse and store data
    while True:
        line = p.stdout.readline()

        loglinetxt = line
        new_posts = [{"loglinetxt": loglinetxt,
                      "host": HOST,
                      "logpath": LOG_PATH,
                      "collection_name":COLLECTION_NAME}]

        mongo_coll.insert(new_posts)


if __name__ == '__main__':
    main()
