#!/bin/python

#################################################################################
#                          check_elasticsearch.py                               #
#               script to check health of elasticsearch_cluster                 #
#           it is also possible to check a query and set thresholds             #
#                   and you can also analyze top hits                           #
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
EXIT_OK = 0
EXIT_WARNING = 1
EXIT_CRITICAL = 2
EXIT_UNKNOWN = 3

# check the health
def health(data_url):
    '''checks the general health of the elastic cluster'''
    es = json.load(urllib.urlopen(str(data_url) + '/_cluster/health'))
    icingaout = 'timed_out:%s;nodes:%s;data_nodes:%s;active_primary_shards%s;active_shards:%s;relocating_shards:%s;initializing_shards:%s;unassigned_shards:%s;' \
    % (es['timed_out'],es['number_of_nodes'],es['number_of_data_nodes'],es['active_primary_shards'],es['active_shards'],es['relocating_shards'],es['initializing_shards'],es['unassigned_shards'])
    message = ': Cluster: %s | %s' % (es['status'], icingaout)
    if es["status"] == "red":
        critical_exit(message)
    elif es["status"] == "orange":
        warning_exit(message)
    elif es["status"] == "green":
        ok_exit(message)

# check a query
def metric(data_url, index, query, critical, warning, invert, duration, top, field):
    infodata = '\n'
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

    try:
        if top is not None:
            searchstring = '{\
                "size": 0,\
                "query": {\
                    "filtered": {\
                        "query": {\
                            "query_string":{\
                                "query":"' + query + '",\
                                "default_field":"_all"\
                            }\
                        },\
                        "filter":{\
                            "range":{\
                                "@timestamp":{\
                                    "from":"now' + duration + '",\
                                    "to":"now"\
                                }\
                            }\
                        }\
                    }\
                },\
                "aggs": {\
                    "top-tags": {\
                        "terms": {\
                            "field": "' + field + '",\
                            "size":' + int(top) + '\
                        }\
                    }\
                }\
            }'
            query_data = json.load(urllib.urlopen(str(data_url) + '/' + str(index) + '/_search?search_type=count' , data=searchstring))
            hits = int(query_data['hits']['total'])
            for info in query_data['aggregations']['top-tags']['buckets']:
                infodata = infodata + str(field)+'_'+ str(info['key']) + ': has ' + str(info['doc_count']) + ' hits \n'
            message = ': "%s" returned %s (over %s) %s| query=%s; warning=%s; critical=%s' % (query, hits, duration, infodata, hits, warning, critical)
        else:
            query_data = json.load(urllib.urlopen(str(data_url) + '/' + str(index) + '/_search?search_type=count' , data=searchstring))
            hits = int(query_data['hits']['total'])
            message = ': "%s" returned %s (over %s) | query=%s; warning=%s; critical=%s' % (query, hits, duration, hits, warning, critical)

        if invert:
            if hits < critical:
                critical_exit(message)
            if hits < warning:
                warning_exit(message)
        else:
            if hits > critical:
                critical_exit(message)
            if hits > warning:
                warning_exit(message)
        ok_exit(message)
    except:
        unknown_exit("something went wrong")

# icinga returncode functions
def critical_exit(message):
    '''returns icinga critical'''
    print 'CRITICAL %s' % message
    sys.exit(EXIT_CRITICAL)

def warning_exit(message):
    '''returns icinga warning'''
    print 'WARNING %s' % message
    sys.exit(EXIT_WARNING)

def ok_exit(message):
    '''returns icinga ok'''
    print 'OK %s' % message
    sys.exit(EXIT_OK)

def unknown_exit(message):
    '''returns icinga unknown'''
    print 'UNKNOWN %s' % message
    sys.exit(EXIT_UNKNOWN)

if __name__ == '__main__':
    # request parameters for script
    parser = argparse.ArgumentParser('Icinga check for elasticsearch')
    parser.add_argument('--host', required=True, help='elasticsearch host')
    parser.add_argument('--port', type=int, default=9200, help='port that elasticsearch is running on (eg. 9200)')
    parser.add_argument('--uri', default='', help='Uri for elasticsearch for example /elasticsearch')
    parser.add_argument('--command', default='health', choices=['health','metric'], help='check command')
    parser.add_argument('--index', default='logstash-*', help='the index you want to query for example logstash-*')
    parser.add_argument('--query', help='e.g: source:localhorst AND message:login failed')
    parser.add_argument('--critical', type=int, help='Critical threshold, e.g. 1, 100')
    parser.add_argument('--warning', type=int, help='Warning threshold, e.g. 1, 20')
    parser.add_argument('--invert', action='store_true', help='Invert the check so that an alert is triggered if the value falls below the threshold. Invert is implied if warning threshold > critical threshold')
    parser.add_argument('--duration', default='5m', help='e.g: 1h, 15m, 32d')
    parser.add_argument('--top', type=int, help='Display top hits for query')
    parser.add_argument('--field', help='Name of the field you want to have in your top analysis')
    args = parser.parse_args()
    try:
        data_url = "http://" + str(args.host) + ":" + str(args.port) + "/" + str(args.uri)
    except:
        print "something went wrong with the url shit"
    # logic to call the right functions
    if args.command=="metric":
        metric(data_url, args.index, args.query, args.critical, args.warning, args.invert, args.duration, args.top, args.field)
    else:
        health(data_url)
