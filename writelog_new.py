'''
Created on Dec 16, 2014

@author: alberto

Created on Dec 12, 2014

@author: alberto
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
COLLECTION_NAME = 'jasper_new'
MAX_COLLECTION_SIZE = 5  # in megabytes


def main():
    # connect to mongodb

    mongo_conn = Connection()
    mongo_db = mongo_conn[DB_NAME]
    try:
        mongo_coll = mongo_db.create_collection(COLLECTION_NAME,
                                                capped=True,
                                                size=MAX_COLLECTION_SIZE * 1048576)
    except CollectionInvalid:
        mongo_coll = mongo_db[COLLECTION_NAME]

    # open remote log file
    cmd = 'tail -f f:\jasperserver.log'
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
    # parse and store data
    while True:
        line = p.stdout.readline()
        data = parse_line(line)
#        new_posts = [{"loglinetxt": loglinetxt,
#                      "host": HOST,
#                      "logpath": LOG_PATH,
#                      "collection_name": COLLECTION_NAME}]
#        mongo_coll.insert(new_posts)

def parse_line(line):
    #    m = re.search('controls', line)
    #   ('(?<=abc)def', 'abcdef')
    m = re.search('(?<=coyote)', line)
    if m:
        #        print "m.group() : ", m.group()
        #        print "m.group(1) : ", m.group(1)
        #        print "m.group(2) : ", m.group(2)
        print("found a match!")

    else:
        print ("no match")
        return {}


if __name__ == '__main__':
    main()
