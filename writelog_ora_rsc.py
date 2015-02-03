'''
#-------------------------------------------------------------------------------
# Name:        writelog mongodb con replicaset
# Purpose:
#
# Author:      alberto.frosi
#
# Created:     03/02/2015
# Copyright:   (c) alberto.frosi 2015
# Licence:    Use of this source code is governed by a BSD-style
#-------------------------------------------------------------------------------
#!/usr/bin/env python
'''
import re
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT
from pymongo import Connection
from pymongo.errors import CollectionInvalid
from pymongo.mongo_replica_set_client import MongoReplicaSetClient
rsc = MongoReplicaSetClient('albertofro-insp:27001,albertofro-insp:27002, albertofro-insp:27003', replicaSet='test')
import pymongo

HOST = 'AF-HP'
LOG_PATH = '/home/alberto/alert_kira1.log'
DB_NAME = 'mydb'
COLLECTION_NAME = 'oraclelog'
MAX_COLLECTION_SIZE = 5 # in megabytes
from pymongo import MongoClient, ReadPreference
rsc = MongoClient("albertofro-insp:27002", replicaset='test')

def main():

    #   var myDateString = Date();
    # open remote log file
    cmd = 'sshpass -p "123" ssh -o StrictHostKeyChecking=no abc@stellar "tail -f -n 1000000 /./alert_xxx.log"'

    p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)

    while True:
        line = p.stdout.readline()
        loglinetxt = parse_line(line)



def parse_line(line):

    #    m = re.search('controls', line)
    #   ('(?<=abc)def', 'abcdef')
    m = re.search('(?<=ORA-)', line)

    if m:

        print("found a match!")
        #print(today)


        print line.split(" ")
        #        a,b = line.split(": ")
        ora = line.split(" ")
        a,b,= ora[0],ora[1]
        print a
        print b

        DB_NAME = 'mydb'
        COLLECTION_NAME = 'oraclelog'
        db = rsc.mydb
        collection = db.oraclelog
        document = [{"loglinetxt": line,
                     "host": HOST,
                     "logpath": LOG_PATH,
                     "collection_name":COLLECTION_NAME,
                     "ORA": a,
                     "DESC": b,
                     "data" :datetime.now()}]
        collection.insert(document)

    else:
        print(" No found a match!")


if __name__ == '__main__':
    main()



