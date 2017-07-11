#!/bin/env python
'''check for UAR/FLASH-FAILURE'''

import sys
import os
#import argparse

# icinga returncode vars
EXIT_OK = 0
EXIT_CRITICAL = 2
EXIT_UNKNOWN = 3

flashfile = "/var/tmp/flash_uar.log"

def is_globalzone():
    zonename = os.popen("zonename").read().splitlines()
    if any('global' in x for x in zonename):
        return(True)
    else:
        return(False)

def message(outputList):
    print outputList

def parse_flashlogfile(flashlogfile):
    with open(flashlogfile) as f:
        content = f.read().splitlines()
    if any('EXIT=0' in x for x in content):
        message(str(content))
        ok_exit()
    else:
        message(str(content))
        critical_exit()

# icinga returncode functions
def critical_exit():
    sys.exit(EXIT_CRITICAL)

def ok_exit():
    sys.exit(EXIT_OK)

def unknown_exit():
    sys.exit(EXIT_UNKNOWN)

if __name__ == '__main__':
    # request parameters for script
    #parser = argparse.ArgumentParser('Icinga check for UAR/FLASH-FAILURE')
    #parser.add_argument('--flashfile', default='/var/tmp/flash_uar.log', help='path to uar/flash log file. --> /var/tmp/flash_uar.log')
    #args = parser.parse_args()
    # first check if this is the global zone
    if is_globalzone():
        parse_flashlogfile(flashfile)
    else:
        print "this is not the global zone"
        ok_exit()
