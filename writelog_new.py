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

HOST = 'OEL65'
LOG_PATH = '/home/oracle/jasperreports-server-cp-5.6.0/apache-tomcat/logs/localhost_access_log.2014-10-07.txt'
DB_NAME = 'mydb'
COLLECTION_NAME = 'jasper1'
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
        data = parse_line(line)
#       ciccio ciccio = line
##        new_posts = [{"author": data,
##               "text": "123",
##               "tags": "abc"}]
##
##        mongo_coll.insert(new_posts)
def parse_line(line):
    #    m = re.search('controls', line)

    m = re.search( r'(.*)controls(.*?) .*', line, re.M|re.I)
    if m:
        print "m.group() : ", m.group()
        print "m.group(1) : ", m.group(1)
        print "m.group(2) : ", m.group(2)
        print("found a match!")


    else:
        print ("no match")
        return {}



if __name__ == '__main__':
    main()