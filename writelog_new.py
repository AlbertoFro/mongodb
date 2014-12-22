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
LOG_PATH = '/home/alberto/Documenti/Win7SP1/jasperserver1.log'
DB_NAME = 'mydb'
COLLECTION_NAME = 'jasperok'
MAX_COLLECTION_SIZE = 5 # in megabytes
#today = datetime.date.today()


def main():


    # open remote log file
    cmd = 'tail -f /home/alberto/Documenti/Win7SP1/jasperserver1.log'
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)

    while True:
        line = p.stdout.readline()
        loglinetxt = parse_line(line)



def parse_line(line):

    #    m = re.search('controls', line)
    #   ('(?<=abc)def', 'abcdef')
    m = re.search('(?<=ERROR)', line)

    if m:

        print("found a match!")
        #print(today)

        DB_NAME = 'mydb'
        COLLECTION_NAME = 'jasperok'
        mongo_conn = Connection()
        mongo_db = mongo_conn[DB_NAME]
        mongo_coll = mongo_db[COLLECTION_NAME]
        new_posts = [{"loglinetxt": line,
                      "host": HOST,
                      "logpath": LOG_PATH,
                      "collection_name":COLLECTION_NAME}]

        mongo_coll.insert(new_posts)

    else:
        print(" No found a match!")


if __name__ == '__main__':
    main()

