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

HOST = 'AF-HP'
LOG_PATH = 'f:\jasperserver.log'
DB_NAME = 'mydb'
COLLECTION_NAME = 'jasperlog1'
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
    cmd = 'tail -f f:\jasperserver.log'
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
    # parse and store data



    while True:

        line = p.stdout.readline()

        loglinetxt = parse_line(line)

        new_posts = [{"loglinetxt": line,
                      "host": HOST,
                      "logpath": LOG_PATH,
                      "collection_name":COLLECTION_NAME}]

        mongo_coll.insert(new_posts)



def parse_line(line):

    #    m = re.search('controls', line)
    #   ('(?<=abc)def', 'abcdef')
    m = re.search('(?<=AuthenticatorBase)', line)

    if m:
        #print m.group()
        print("found a match!")


    else:
        print(" No found a match!")
        return False




if __name__ == '__main__':
    main()
