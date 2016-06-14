#!/bin/python

#################################################################################
#                          check_elasticsearch.py                               #
#               script to check health of elasticsearch_cluster                 #
#           it is also possible to check a query and set thresholds             #
#################################################################################

'''

check_elasticsearch_cluster.py
Copyright (C) 2016  langer.markus@gmail.com

'''

import sys
import json
import urllib
import argparse

# icinga returncode vars
EXIT_OK         = 0
EXIT_WARNING    = 1
EXIT_CRITICAL   = 2
EXIT_UNKNOWN    = 3

# check the health
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
    message = ': Cluster: ' + str(elasticsearch_cluster["status"]) + ' | ' + str(icingaout)
    if elasticsearch_cluster["status"] == "red":
        critical_exit(message, info=None)
    elif elasticsearch_cluster["status"] == "orange":
        warning_exit(message, info=None)
    elif elasticsearch_cluster["status"] == "green":
        ok_exit(message, info=None)

# check a query
def metric(data_url, query, critical, warning, invert, duration):
    searchstring = '{\
            "query":{\
                "filtered":{\
                    "query":{ \
                        "query_string":{\
                            "query":"' + query + '",\
                            "default_field":"_all"\
                        }\
                    },\
                    "filter":{\
                        "range":{\
                            "@timestamp":{\
                                "from":"now-' + duration + '",\
                                "to":"now"\
                            }\
                        }\
                    }\
                }\
            },\
            "from":0}'

    query_data = json.load(urllib.urlopen(str(data_url) + '/logstash-*/_search?search_type=count' , data=searchstring))
    hits = int(query_data['hits']['total'])
    message = ': "%s" returned %s (over %s) | query=%s; warning=%s; critical=%s' % (query, hits, duration, hits, warning, critical)
    info = 'critical %s %s' % ('<' if invert else '>', critical)
    if warning is not None:
        info += '\nwarning %s %s' % ('<' if invert else '>', warning)

    if invert:
        if hits < critical:
            critical_exit(message, info)
        if hits < warning:
            warning_exit(message, info)
    else:
        if hits > critical:
            critical_exit(message, info)
        if hits > warning:
            warning_exit(message, info)

    ok_exit(message)

# icinga returncode functions
def critical_exit(message, info=None):
    print 'CRITICAL %s' % message
    if info:
        print '\n%s' % info
    sys.exit(EXIT_CRITICAL)

def warning_exit(message, info=None):
    print 'WARNING %s' % message
    if info:
        print '\n%s' % info
    sys.exit(EXIT_WARNING)

def ok_exit(message, info=None):
    print 'OK %s' % message
    if info:
        print '\n%s' % info
    sys.exit(EXIT_OK)

def unknown_exit(message, info=None):
    print 'UNKNOWN %s' % message
    if info:
        print '\n%s' % info
    sys.exit(EXIT_UNKNOWN)

if __name__ == '__main__':
    # request parameters for script
    parser = argparse.ArgumentParser('Icinga check for elasticsearch')
    parser.add_argument('--host', required=True, help='elasticsearch host')
    parser.add_argument('--port', type=int, default=9200, help='port that elasticsearch is running on (eg. 9200)')
    parser.add_argument('--uri', help='Uri for elasticsearch for example /elasticsearch')
    parser.add_argument('--command', default='health', choices=['health','metric'], help='check command')
    parser.add_argument('--query', help='e.g: source:localhorst AND message:login failed')
    parser.add_argument('--critical', type=int, help='Critical threshold, e.g. 1, 100')
    parser.add_argument('--warning', type=int, help='Warning threshold, e.g. 1, 20')
    parser.add_argument('--invert', action='store_true', help='Invert the check so that an alert is triggered if the value falls below the threshold. Invert is implied if warning threshold > critical threshold')
    parser.add_argument('--duration', default='5m', help='e.g: 1h, 15m, 32d')
    args = parser.parse_args()
    try:
        data_url = "http://" + str(args.host) + ":" + str(args.port) + "/" + str(args.uri)
    except:
        print "something went wrong with the url shit"
    # logic to call the right functions
    if args.command=="metric":
        metric(data_url, args.query, args.critical, args.warning, args.invert, args.duration)
    else:
        health(data_url)
