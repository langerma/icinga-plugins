#!/bin/env python

import sys
import argparse
import subprocess

# icinga returncode vars
EXIT_OK         = 0
EXIT_WARNING    = 1
EXIT_CRITICAL   = 2
EXIT_UNKNOWN    = 3

def fetch_stats(dcliArgs):
    rdsinfoOutput = subprocess.Popen(rdsinfoArgs, stdout=subprocess.PIPE, shell=True).communicate()[0]
    if len(rdsinfoOutput):
        return rdsinfoOutput

def parse_rdsinfo(output, warning, critical):
    outputList=output.splitlines()
    analyzedList=[]
    #print outputList
    for line in outputList:
        lineList = line.split()
        analyzedList.append(lineList)

    analyzedList=filter(None, analyzedList)
    print analyzedList

# icinga returncode functions
def critical_exit():
    sys.exit(EXIT_CRITICAL)

def warning_exit():
    sys.exit(EXIT_WARNING)

def ok_exit():
    sys.exit(EXIT_OK)

def unknown_exit():
    sys.exit(EXIT_UNKNOWN)

if __name__ == '__main__':
    # request parameters for script
    parser = argparse.ArgumentParser('Icinga check for rds-info')
    parser.add_argument('--rdsinfo', default='/usr/bin/rds-info', help='path to rds-info. /usr/bin/rdsinfo')
    parser.add_argument('--warning', default=90, type=int, help='warning threshold: default=90')
    parser.add_argument('--critical', default=95, type=int, help='critical threshold: default=95')

    args = parser.parse_args()
    rdsinfoArgs = str(args.rdsinfo) + " -Icn" # | egrep 'send_queue_full|ib_tx_ring_full"
    rdsinfoStats = fetch_stats(rdsinfoArgs)
    parse_rdsinfo(rdsinfoStats, args.warning, args.critical)

