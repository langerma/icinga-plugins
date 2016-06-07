#!/usr/bin/python

###############################################################################
#                             check_file_age.py                               #
#                       (c) langer.markus@gmail.com                           #
#     checks the age of files and paths you also can add a threshold          #
###############################################################################

import sys
import os
import time
import datetime
import argparse

def thresholds(timedelta, warning, critical):
    warning = (warning * 3600)
    critical = (critical * 3600)
    if timedelta < critical and timedelta > warning:
        status = "WARNING"
        perfstring=" | current_age=" + str(timedelta) + ";" + str(warning) + ";" + str(critical)
        print "Fileage " + status + " " + str(datetime.timedelta(seconds=timedelta)) + ";" + perfstring
        sys.exit(1)
    elif timedelta > warning and timedelta > critical:
        status = "CRITCAL"
        perfstring=" | current_age=" + str(timedelta) + ";" + str(warning) + ";" + str(critical)
        print "Fileage " + status + " " + str(datetime.timedelta(seconds=timedelta)) + ";" + perfstring
        sys.exit(2)
    elif timedelta < warning and timedelta < critical:
        status = "OK"
        perfstring=" | current_age=" + str(timedelta) + ";" + str(warning) + ";" + str(critical)
        print "Fileage " + status + " " + str(datetime.timedelta(seconds=timedelta)) + ";" + perfstring
        sys.exit(0)

def check(filename, text, method, warning, critical):
    current_time = time.time()
    if method == 'accessed':
        fileage = os.path.getatime(filename)
        fileage_relative = int(current_time) - int(fileage)
        #print str(text) + str(time.ctime(fileage)) + " relative time: " + str(datetime.timedelta(seconds=fileage_relative))
        thresholds(fileage_relative, warning=warning, critical=critical)
    elif method == 'metadata':
        fileage = os.path.getmtime(filename)
        fileage_relative = int(current_time) - int(fileage)
        #print str(text) + str(time.ctime(fileage)) + " relative time: " + str(datetime.timedelta(seconds=fileage_relative))
        thresholds(fileage_relative, warning=warning, critical=critical)
    elif method == 'modified':
        fileage = os.path.getctime(filename)
        fileage_relative = int(current_time) - int(fileage)
        #print str(text) + str(time.ctime(fileage)) + " relative time: " + str(datetime.timedelta(seconds=fileage_relative))
        thresholds(fileage_relative, warning=warning, critical=critical)
    else:
        print "Error: false method"

if  __name__ == '__main__':
    parser = argparse.ArgumentParser('Icinga check for fileage')
    parser.add_argument('--filename', required=True, help='filename or path')
    parser.add_argument('--text', default='last modified on: ', help='Custom Text (e.g. last modified on:)')
    parser.add_argument('--method', default='modified', choices=['modified','accessed','metadata'], help='Method what you want to check')
    parser.add_argument('--warning', default=24, help='Warning threshold in hours')
    parser.add_argument('--critical', default=48, help='Critical threshold in hours')
    args = parser.parse_args()
    check(filename=args.filename,
            text=args.text,
            method=args.method,
            warning=args.warning,
            critical=args.critical)
