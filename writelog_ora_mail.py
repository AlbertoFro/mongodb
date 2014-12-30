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
# Aggiunti per gestione mail
import sys
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import socket
import time
from smtplib import SMTPException

HOST = 'AF-HP'
LOG_PATH = '/home/alberto/Documenti/Win7SP1/tst.log'
DB_NAME = 'mydb'
COLLECTION_NAME = 'jasperok'
MAX_COLLECTION_SIZE = 5 # in megabytes
#today = datetime.date.today()


def main():


    # open remote log file
    cmd = 'tail -n 1000000 -f /home/alberto/Documenti/Win7SP1/tst.log'
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
        COLLECTION_NAME = 'jasperok'
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

        #mando mail
        sender = 'admin_psutil@xxxx.com'
        receivers = 'alberto.frosi@xxxx.com'

        msg = MIMEMultipart()
        msg['From'] = 'admin_psutil@xxx.com'
        msg['To'] = 'alberto.frosi@xxx.com'
        msg['Subject'] = 'Check space Disk C:\ for'
        message = 'Attenzione spazio su disco C:\ insufficiente '
        msg.attach(MIMEText(message))
        try:
            smtpObj = smtplib.SMTP('xxxx.bbbb.it',NN)
            smtpObj.sendmail(sender, receivers, msg.as_string())
            print ("Successfully sent email")
            print(socket.gethostname())
        except smtplib.SMTPException:
            print("Error: unable to send email")


    else:
        print(" No found a match!")


if __name__ == '__main__':
    main()
