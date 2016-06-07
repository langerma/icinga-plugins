#!/usr/bin/python

###############################################################################
#                             check_file_age.py                               #
#                       (c) langer.markus@gmail.com                           #
###############################################################################

import sys
import os
import time
import datetime
import argparse


def check(filename, text, method):
    current_time = time.time()
    if method == 'accessed':
        fileage = os.path.getatime(filename)
        fileage_relative = int(current_time) - int(fileage)
        print str(text) + str(time.ctime(fileage)) + " relative time: " + str(datetime.timedelta(seconds=fileage_relative))
        sys.exit(0)
    elif method == 'metadata':
        fileage = os.path.getmtime(filename)
        fileage_relative = int(current_time) - int(fileage)
        print str(text) + str(time.ctime(fileage)) + " relative time: " + str(datetime.timedelta(seconds=fileage_relative))
        sys.exit(0)
    elif method == 'modified':
        fileage = os.path.getctime(filename)
        fileage_relative = int(current_time) - int(fileage)
        print str(text) + str(time.ctime(fileage)) + " relative time: " + str(datetime.timedelta(seconds=fileage_relative))
        sys.exit(0)
    else:
        print "Error: false method"

if  __name__ == '__main__':
    parser = argparse.ArgumentParser('Icinga check for fileage')
    parser.add_argument('--filename', required=True, help='filename or path')
    parser.add_argument('--text', default='last modified on: ', help='Custom Text (e.g. last modified on:)')
    parser.add_argument('--method', default='modified', choices=['modified','accessed','metadata'], help='Method what you want to check')
    args = parser.parse_args()
    check(filename=args.filename,text=args.text,method=args.method)
