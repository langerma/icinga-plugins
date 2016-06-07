#!/bin/python

#################################################################################
#                          check_elasticsearch.py                               #
#       script to check cluster and nodestates of elasticsearch                 #
#################################################################################

'''

check_elasticsearch_cluster.py
Copyright (C) 2016  langer.markus@gmail.com

# searchstring

{
    "query": {
        "match": {
            "netflow.output_snmp": {
                "query": 14,
                "type": "phrase"
            }
        }
        "filter": {
            "range": {
                {field-name}: {
                    "from": {lower-value}
                    "to": {upper-value}
                }
            }
        }
    }
}

{
    "query": {
        "filtered": {
            "query": {"match_all": {}},
            "filter": {
                "and": [
                    {"term": {"netflow.output_snmp": "14"}},
                    {"term": {"books.genre": "scifi"}}
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

def health(elasticsearch_host, elasticsearch_port):
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

def field():
    #json.load(urllib.urlopen(elasticsearch, data=searchstring))
    pass

    #def main():
    #    try:
    #        elasticsearch_check = str(args[1])
    #        if elasticsearch_check == "health":
    #            #elasticsearch_host = str(args[2])
    #            #elasticsearch_port = str(args[3])
    #            health(str(args[2]),str(args[3]))
    #    except:
    #        print "shit happens -- too few parameters"
    #        sys.exit(5)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Icinga check for elasticsearch')
    parser.add_argument('--host', required=True, help='elasticsearch host')
    parser.add_argument('--port', type=int, help='port that elasticsearch is running on (eg. 9200)')
    parser.add_argument('--uri', help='Uri for elasticsearch for example /elasticsearch')
    parser.add_argument('--command', default='health', choices=['health','metric'], help='check command')
    parser.add_argument('--field', help='Field you want to check e.g. logins_failed')
    parser.add_argument('--critical', help='Critical threshold, e.g. 1, 100')
    parser.add_argument('--warning', help='Warning threshold, e.g. 1, 20')
    parser.add_argument('--duration', type=int, default=5, help='Number of minutes of data to aggregate')
    args = parser.parse_args()
    if args.command == "health":
        pass
    else:
        health(elasticsearch_string)

    #check(host=args.host,
    #      metric=args.metric,
    #      warning_threshold=args.warning,
    #      critical_threshold=args.critical,
    #      invert=args.invert,
    #      function=args.function,
    #      duration=args.duration,
    #      user=args.user,
    #      password=args.password,
    #      grafana=args.grafana,
    #      datasourceid=args.datasourceid,
    #      authkey=args.authkey)
