#!/bin/python

#################################################################################
#                          check_elasticsearch.py                               #
#       script to check cluster and nodestates of elasticsearch                 #
#################################################################################

import sys
import json
import urllib
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-h", "--host", type=str, help="elasticsearch host")
parser.add_argument("-n", "--nodename", type=str, help="nodename")
parser.add_argument("-p", "--port", type=str, help="elasticsearch port")

args=parser.parse_args()

elasticsearch_host = args.host
elasticsearch_node = args.nodename
elasticsearch_port = arps.port

data_url= str(elasticsearch_host) + ":" + "/node/" + str(jenkins_jobname) + str(jenkins_api)

#print "getting data from:" + str(data_url)

data = json.load(urllib.urlopen(data_url))

lastBuild = int(data["lastBuild"]["number"])
lastStableBuild = int(data["lastStableBuild"]["number"])
lastUnsuccessfulBuild = int(data["lastUnsuccessfulBuild"]["number"])

failedBuilds = lastUnsuccessfulBuild - lastStableBuild
if failedBuilds < 0:
    failedBuilds = 0

if failedBuilds == 0:
    print str(jenkins_jobname) + " OK: " + str(failedBuilds) + " failed builds | " + str(failedBuilds)
    sys.exit(0)
elif failedBuilds > 2:
    print str(jenkins_jobname) + " CRITICAL: " + str(failedBuilds) + " failed builds | " + str(failedBuilds)
    sys.exit(2)
elif failedBuilds > 0:
    print str(jenkins_jobname) + " WARNING: " + str(failedBuilds) + " failed builds | " + str(failedBuilds)
    sys.exit(1)

