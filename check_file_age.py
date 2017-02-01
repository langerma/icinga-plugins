#!/usr/bin/python

###############################################################################
#                             check_file_age.py                               #
#                       (c) langer.markus@gmail.com                           #
#     checks the age of files and paths you also can add a threshold          #
###############################################################################

import sys
import os
import time
import argparse

# icinga returncode vars
EXIT_OK = 0
EXIT_WARNING = 1
EXIT_CRITICAL = 2
EXIT_UNKNOWN = 3


def thresholds(filename, timedelta, warning, critical):
    warning = (warning * 3600)
    critical = (critical * 3600)
    message = '- %s is %s old |current_age=%s;warning=%s;critical=%s' % (
            filename,
            timedelta,
            timedelta,
            warning,
            critical)
    if timedelta > critical:
        critical_exit(message)
    if timedelta > warning:
        warning_exit(message)
    ok_exit(message)


def check(filename, method, warning, critical):
    current_time = time.time()
    if method == 'accessed':
        fileage = os.path.getatime(filename)
    elif method == 'metadata':
        fileage = os.path.getmtime(filename)
    elif method == 'modified':
        fileage = os.path.getctime(filename)
    else:
        unknown_exit("Error: false method")

    timedelta = int(current_time) - int(fileage)
    thresholds(
            filename=filename,
            timedelta=timedelta,
            warning=warning,
            critical=critical)


# icinga returncode functions
def critical_exit(message):
    print 'CRITICAL %s' % message
    sys.exit(EXIT_CRITICAL)


def warning_exit(message):
    print 'WARNING %s' % message
    sys.exit(EXIT_WARNING)


def ok_exit(message):
    print 'OK %s' % message
    sys.exit(EXIT_OK)


def unknown_exit(message):
    print 'UNKNOWN %s' % message
    sys.exit(EXIT_UNKNOWN)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Icinga check for fileage')
    parser.add_argument('--filename', required=True, help='filename or path')
    parser.add_argument(
            '--method',
            default='modified',
            choices=['modified', 'accessed', 'metadata'],
            help='Method what you want to check')
    parser.add_argument(
            '--warning',
            default=24,
            type=int,
            help='Warning threshold in hours')
    parser.add_argument(
            '--critical',
            default=48,
            type=int,
            help='Critical threshold in hours')
    args = parser.parse_args()
    check(
            filename=args.filename,
            method=args.method,
            warning=args.warning,
            critical=args.critical)
