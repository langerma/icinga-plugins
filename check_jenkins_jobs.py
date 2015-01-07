#!/bin/python

####################################################################################
#                           check_jenkins_jobs.py                                  #
#             script that checks build fails on jenkins jobs                       #
####################################################################################
""" 
    first approach of checking build status via jenkins json api. 
    for the moment it works but some work has to be done --> 
    parameters and cli switches and shit. make it work, make it right, make it fast 
"""


import sys
import json
import urllib
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-u", "--url", type=str, help="jenkins url")
parser.add_argument("-j", "--job", type=str, help="jenkins jobname")
#parser.add_argument("-v", "--verbosity", type=int, choices=[0,1,2], help="debug output"
args=parser.parse_args()

#jenkins_url = "https://jenkins.int.jumio.com/"
#jenkins_jobname = "sam_monitoring"
#jenkins_jobname = "ops_puppet_release_internal"
jenkins_api = "/api/json"
jenkins_url = args.url
jenkins_jobname = args.job

data_url= str(jenkins_url) + "job/" + str(jenkins_jobname) + str(jenkins_api)

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

