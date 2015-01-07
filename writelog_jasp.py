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
LOG_PATH = '/home/alberto/jasperserver.log'
DB_NAME = 'mydb'
COLLECTION_NAME = 'jasperlog'
MAX_COLLECTION_SIZE = 5 # in megabytes
#today = datetime.date.today()


def main():


    # open remote log file
    cmd = 'tail -n 1000000 -f /home/albertofro/jasperserver.log'
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
        COLLECTION_NAME = 'jasperlog'
        mongo_conn = Connection()
        mongo_db = mongo_conn[DB_NAME]
        mongo_coll = mongo_db[COLLECTION_NAME]
        new_posts = [{"loglinetxt": line,
                      "host": HOST,
                      "logpath": LOG_PATH,
                      "collection_name":COLLECTION_NAME,
                      "ORA": a,
                      "DESC": b}]

        mongo_coll.insert(new_posts)

    else:
        print(" No found a match!")


if __name__ == '__main__':
    main()



