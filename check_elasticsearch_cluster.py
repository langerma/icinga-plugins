#!/bin/python

#################################################################################
#                          check_elasticsearch.py                               #
#       script to check cluster and nodestates of elasticsearch                 #
#################################################################################

'''

check_elasticsearch_cluster.py
Copyright (C) 2016  langer.markus@gmail.com

# simple searchstring for timerange

{
    "range" : {
        "timestamp" : {"gt" : "now-1h"}
    }
}

# combined searchstring 

{
    "query": {
        "filtered": {
            "query": {
                "match_all": {}
            },
            "filter": {
                "and": [
                    {
                        "range" : {
                            "timestamp" : { 
                                "gt" : "now-15m"
                            }
                        },
                    },
                    {
                        "term": {
                            "field": "value"
                        }
                    }
                ]
            }
        }
    }
}

json.load(urllib.urlopen('http://www.langerma.org/elasticsearch/_search?search_type=count', data='searchstring'))



'''

import sys
import json
import urllib
import argparse
import pprint

def health(data_url):
    elasticsearch_cluster = json.load(urllib.urlopen(str(data_url) + '/_cluster/health'))
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

def metric(data_url, field, value, critical, warning, duration):
    searchstring = '{"sort": {"date": "asc"}}'

    query_data = json.load(urllib.urlopen(str(data_url) + '/_all/_search' , data=searchstring))
    pprint.pprint(query_data)

if __name__ == '__main__':
    # request parameters for script
    parser = argparse.ArgumentParser('Icinga check for elasticsearch')
    parser.add_argument('--host', required=True, help='elasticsearch host')
    parser.add_argument('--port', type=int, default=9200, help='port that elasticsearch is running on (eg. 9200)')
    parser.add_argument('--uri', help='Uri for elasticsearch for example /elasticsearch')
    parser.add_argument('--command', default='health', choices=['health','metric'], help='check command')
    parser.add_argument('--field', help='Field you want to check e.g. logins_failed')
    parser.add_argument('--value', help='Query this value')
    parser.add_argument('--critical', help='Critical threshold, e.g. 1, 100')
    parser.add_argument('--warning', help='Warning threshold, e.g. 1, 20')
    parser.add_argument('--duration', default=5, help='e.g: 1h, 15m, 32d')
    args = parser.parse_args()
    try:
        data_url = "http://" + str(args.host) + ":" + str(args.port) + "/" + str(args.uri)
    except:
        print "something went wrong with the url shit"
    # logic to call the right functions
    if args.command=="metric":
        metric(data_url, args.field, args.value, args.critical, args.warning, args.duration)
    else:
        health(data_url)
