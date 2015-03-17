#!/bin/python

#################################################################################
#                          check_elasticsearch.py                               #
#       script to check cluster and nodestates of elasticsearch                 #
#################################################################################

import sys
import json
import urllib

args = sys.argv

elasticsearch_host = str(args[1])
elasticsearch_port = str(args[2])

data_url = "http://" + str(elasticsearch_host) + ":" + str(elasticsearch_port) + "/_cluster/health"

elasticsearch_cluster = json.load(urllib.urlopen(data_url))

icingaout = "timed out: " + str(elasticsearch_cluster["timed_out"]) + \
    "; nodes: " + str(elasticsearch_cluster["number_of_nodes"]) + \
    "; data nodes: " + str(elasticsearch_cluster["number_of_data_nodes"]) + \
    "; active primary shards: " + str(elasticsearch_cluster["active_primary_shards"]) + \
    "; active shards: " + str(elasticsearch_cluster["active_shards"]) + \
    "; relocating shards: " + str(elasticsearch_cluster["relocating_shards"]) + \
    "; init shards: " + str(elasticsearch_cluster["initializing_shards"]) + \
    "; unassigned shards: " + str(elasticsearch_cluster["unassigned_shards"])

if elasticsearch_cluster["status"] == "red":
    print "Cluster: " + str(elasticsearch_cluster["status"])+ " | " + str(icingaout)
    sys.exit(2)
elif elasticsearch_cluster["status"] == "orange":
    print "Cluster: " + str(elasticsearch_cluster["status"])+ " | " + str(icingaout)
    sys.exit(1)
elif elasticsearch_cluster["status"] == "green":
    print "Cluster: " + str(elasticsearch_cluster["status"])+ " | " + str(icingaout)
    sys.exit(0)
