'''

#-------------------------------------------------------------------------------

# Name:        writelog_jasper mongodb

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
from pymongo import MongoClient

# Aggiunti per gestione mail

import sys

import smtplib

from email.MIMEMultipart import MIMEMultipart

from email.MIMEText import MIMEText

import socket

import time

from smtplib import SMTPException

import os

import socket , sys
import logging
import graypy


#HOST = ''




LOG_J = 'jasperserver.log'

DB_NAME = 'mydb'

COLLECTION_NAME = 'jasperok'

MAX_COLLECTION_SIZE = 5 # in megabytes


def main():


    cmd_jasper = 'tail -f f:\\jasperserver.log'

    p_jasper = Popen(cmd_jasper, shell=True, stdout=PIPE, stderr=STDOUT)


    while True:

        line_jasper = p_jasper.stdout.readline()
        loglinetxt_j = parse_line_j(line_jasper)


def parse_line_j(line_jasper):



    m_j = re.search('(?<=ORA-)', line_jasper)

    m_j1 = re.search('(?<=ERROR)', line_jasper)

    m_j2 = re.search('(?<=Error executing) ', line_jasper)

#    m_j1 = re.search(' (?<=stack trace of exception that redirected to errorPage.jsp)',line_jasper)

    if m_j1 :


        ora_my_j = line_jasper.split(" ")

        aa,bb,= ora_my_j[0],ora_my_j[1]
        zz = ora_my_j[3]
        if 'errorPage_jsp,http-apr-8081' in zz:
            print('non scrivere!')
        else:

            my_logger = logging.getLogger('jasper')

            my_logger.setLevel(logging.DEBUG)
            handler = graypy.GELFHandler('10.10.10.10', 12201)
            my_logger.addHandler(handler)
            my_logger.handlers = [my_logger.handlers[0], ]
            my_logger.debug(line_jasper)
            #my_logger.info(line_jasper)
            print(line_jasper)
            DB_NAME = 'writelog'
            COLLECTION_NAME = 'writelog_servers'

            mongo_conn = MongoClient("10.10.10.11", 27017)
            mongo_db = mongo_conn[DB_NAME]

            mongo_coll = mongo_db[COLLECTION_NAME]

            new_posts_my = [{"loglinetxt": line_jasper,

                     "host": "HOST.ACME.COM",

                     "logpath": LOG_J,

                     "collection_name":COLLECTION_NAME,

                     "ORA": aa,

                     "DESC": bb,

                     "CAT": "JASPERLOG",

                     "data" :datetime.now()}]

            mongo_coll.insert(new_posts_my)

    if m_j or m_j2:
        ora_my_j = line_jasper.split(" ")
        aa,bb,= ora_my_j[0],ora_my_j[1]

        my_logger = logging.getLogger('jasper')
        my_logger.setLevel(logging.DEBUG)
        handler = graypy.GELFHandler('10.10.10.10', 12201)
        my_logger.addHandler(handler)
        my_logger.handlers = [my_logger.handlers[0], ]
        my_logger.debug(line_jasper)
        print(line_jasper)
        DB_NAME = 'writelog'

        COLLECTION_NAME = 'writelog_servers'

        mongo_conn = MongoClient("10.10.10.11", 27017)

        mongo_db = mongo_conn[DB_NAME]

        mongo_coll = mongo_db[COLLECTION_NAME]

        new_posts_my = [{"loglinetxt": line_jasper,

                         "host": "HOST.ACME.COM",

                         "logpath": LOG_J,

                         "collection_name":COLLECTION_NAME,

                         "ORA": aa,

                         "DESC": bb,

                         "CAT": "JASPERLOG",

                         "data" :datetime.now()}]

        mongo_coll.insert(new_posts_my)

        #       mando_mail()
"""

def mando_mail():

    #mando mail

    sender = 'admin@acme.com'

    receivers = 'albertofro@acme.com'

    msg = MIMEMultipart()

    msg['From'] = 'admin@acme.com'

    msg['To'] = 'albertofro@acme.com'

    msg['Subject'] = "Errore jasperserver.log"

    message = "Verificare jasperserver.log"

    msg.attach(MIMEText(message))

    try:

        smtpObj = smtplib.SMTP('10.10.10.12',25)

        smtpObj.sendmail(sender, receivers, msg.as_string())

        print ("Successfully sent email")

        print(socket.gethostname())

    except smtplib.SMTPException:

        print("Error: unable to send email")


#    else:

#        print(" No found a match!")

"""
if __name__ == '__main__':

    main()




