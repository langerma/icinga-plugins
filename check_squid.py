#!/bin/python

##################################
#       check_squid.py           #
# checks different squid metrics #
##################################

'''

check_squid.py
Copyright (C) 2016  langer.markus@gmail.com

'''

import sys
import os
import time
import cPickle
import argparse
import subprocess

# icinga returncode vars
EXIT_OK = 0
EXIT_WARNING = 1
EXIT_CRITICAL = 2
EXIT_UNKNOWN = 3


def cache_stats(stats, hostname, tmpdir):
    try:
        os.makedirs(tmpdir, 0755)
    except:
        pass
    try:
        cache = open(tmpdir + "/" + hostname, 'w')
        cPickle.dump(stats, cache)
    except:
        pass


def fetch_cached_stats(hostname, pollerinterval, tmpdir):
    mtime = 0
    cachefile = tmpdir + '/' + hostname
    cachelifetime = pollerinterval * 0.75
    now = time.time()
    try:
        mtime = os.stat(cachefile).st_mtime
        if 0 < mtime > (now - cachelifetime):
            cache = open(cachefile, 'r')
            stats = cPickle.load(cache)
            cache.close()
            return stats
    except:
        pass


def fetch_stats(argslist):
    squid5min = subprocess.Popen(argslist + ['mgr:5min'],
                                 stdout=subprocess.PIPE).communicate()[0]
    if len(squid5min):
        return squid5min
    else:
        return False


def filter_stats(stats, query):
    queries = {
        "icp-packets": [
            "icp.pkts_sent",
            "icp.pkts_recv",
        ],
        "icp-requests": [
            "icp.queries_sent",
            "icp.queries_recv",
            "icp.replies_sent",
            "icp.replies_recv",
            "icp.replies_queued",
            "icp.query_timeouts",
        ],
        "icp-transfer": [
            "icp.kbytes_sent",
            "icp.kbytes_recv",
            "icp.q_kbytes_sent",
            "icp.q_kbytes_recv",
            "icp.r_kbytes_sent",
            "icp.r_kbytes_recv",
        ],
        "icp-svctime": [
            "icp.query_median_svc_time",
            "icp.reply_median_svc_time",
        ],
        "requests": [
            "aborted_requests",
            "client_http.requests",
            "client_http.hits",
            "client_http.errors",
            "server.all.requests",
            "server.all.errors",
            "server.http.requests",
            "server.http.errors",
            "server.ftp.requests",
            "server.ftp.errors",
            "server.other.requests",
            "server.other.errors",
        ],
        "transfer": [
            "server.all.kbytes_in",
            "server.all.kbytes_out",
            "server.http.kbytes_in",
            "server.http.kbytes_out",
            "server.ftp.kbytes_in",
            "server.ftp.kbytes_out",
            "server.other.kbytes_in",
            "server.other.kbytes_out",
            "client_http.kbytes_in",
            "client_http.kbytes_out",
        ],
        "svctime": [
            "client_http.all_median_svc_time",
            "client_http.miss_median_svc_time",
            "client_http.nm_median_svc_time",
            "client_http.nh_median_svc_time",
            "client_http.hit_median_svc_time",
            "dns.median_svc_time",
        ],
        "syscallsdisk": [
            "syscalls.disk.opens",
            "syscalls.disk.closes",
            "syscalls.disk.reads",
            "syscalls.disk.writes",
            "syscalls.disk.seeks",
            "syscalls.disk.unlinks",
        ],
        "syscallssocket": [
            "syscalls.sock.accepts",
            "syscalls.sock.sockets",
            "syscalls.sock.connects",
            "syscalls.sock.binds",
            "syscalls.sock.closes",
            "syscalls.sock.reads",
            "syscalls.sock.writes",
            "syscalls.sock.recvfroms",
            "syscalls.sock.sendtos",
        ],
        "swap": [
            "swap.outs",
            "swap.ins",
            "swap.files_cleaned",
        ],
        "unlink": [
            "unlink.requests",
        ],
        "pagefaults": [
            "page_faults",
        ],
        "selectloops": [
            "select_loops",
            "select_fds",
            "average_select_fd_period",
            "median_select_fds",
        ],
        "cpu": [
            "cpu_time",
            "wall_time",
            "cpu_usage",
        ],
    }
    filteredstats = {}
    for item in queries[query]:
        if item in stats:
            filteredstats[item] = stats[item]
    return filteredstats


def output_stats(stats):
    numstats = len(stats)
    for stat in stats:
        numstats -= 1
        output = "%s:" % (stat.replace('.', '_'), )
        if stats[stat] == "U":
            output = output + "U"
        else:
            output = output + ("%.2f" % (float(stats[stat]), ))
        sys.stdout.write(output)
        if numstats > 0:
            sys.stdout.write(" ")


def parse_stats(commandoutput, stats):
    for line in commandoutput.splitlines():
        try:
            name, value = line.split(" = ")
        except:
            continue
        if name in stats:
            length = value.find('/')
            if length < 0:
                length = value.find(' ')
            if length < 0:
                length = value.find('%')
            if length < 0:
                length = None
            stats[name] = value[0:length]
    return stats

stats = {
    "client_http.requests": 0,
    "client_http.hits": 0,
    "client_http.errors": 0,
    "client_http.kbytes_in": 0,
    "client_http.kbytes_out": 0,
    "client_http.all_median_svc_time": 0,
    "client_http.miss_median_svc_time": 0,
    "client_http.nm_median_svc_time": 0,
    "client_http.nh_median_svc_time": 0,
    "client_http.hit_median_svc_time": 0,
    "server.all.requests": 0,
    "server.all.errors": 0,
    "server.all.kbytes_in": 0,
    "server.all.kbytes_out": 0,
    "server.http.requests": 0,
    "server.http.errors": 0,
    "server.http.kbytes_in": 0,
    "server.http.kbytes_out": 0,
    "server.ftp.requests": 0,
    "server.ftp.errors": 0,
    "server.ftp.kbytes_in": 0,
    "server.ftp.kbytes_out": 0,
    "server.other.requests": 0,
    "server.other.errors": 0,
    "server.other.kbytes_in": 0,
    "server.other.kbytes_out": 0,
    "icp.pkts_sent": 0,
    "icp.pkts_recv": 0,
    "icp.queries_sent": 0,
    "icp.replies_sent": 0,
    "icp.queries_recv": 0,
    "icp.replies_recv": 0,
    "icp.replies_queued": 0,
    "icp.query_timeouts": 0,
    "icp.kbytes_sent": 0,
    "icp.kbytes_recv": 0,
    "icp.q_kbytes_sent": 0,
    "icp.r_kbytes_sent": 0,
    "icp.q_kbytes_recv": 0,
    "icp.r_kbytes_recv": 0,
    "icp.query_median_svc_time": 0,
    "icp.reply_median_svc_time": 0,
    "dns.median_svc_time": 0,
    "unlink.requests": 0,
    "page_faults": 0,
    "select_loops": 0,
    "select_fds": 0,
    "average_select_fd_period": 0,
    "median_select_fds": 0,
    "swap.outs": 0,
    "swap.ins": 0,
    "swap.files_cleaned": 0,
    "aborted_requests": 0,
    "syscalls.disk.opens": 0,
    "syscalls.disk.closes": 0,
    "syscalls.disk.reads": 0,
    "syscalls.disk.writes": 0,
    "syscalls.disk.seeks": 0,
    "syscalls.disk.unlinks": 0,
    "syscalls.sock.accepts": 0,
    "syscalls.sock.sockets": 0,
    "syscalls.sock.connects": 0,
    "syscalls.sock.binds": 0,
    "syscalls.sock.closes": 0,
    "syscalls.sock.reads": 0,
    "syscalls.sock.writes": 0,
    "syscalls.sock.recvfroms": 0,
    "syscalls.sock.sendtos": 0,
    "cpu_time": 0,
    "wall_time": 0,
    "cpu_usage": 0
}


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
    # request parameters for script
    parser = argparse.ArgumentParser('Icinga check for Squid Proxy Server')
    parser.add_argument('--squidclient',
                        default='/usr/local/sbin/squidclient',
                        help='path to squidclient')
    parser.add_argument('--tmpdir',
                        default='/tmp/squid-stats',
                        help='temporary file dir')
    parser.add_argument('--hostname',
                        default='localhost',
                        help='Retrieve URL from cache on hostname. \
                                Default is localhost.')
    parser.add_argument('--port',
                        type=int,
                        default=3128,
                        help='Port number of cache.  Default is 3128.')
    parser.add_argument('--timeout',
                        type=int,
                        default=10,
                        help='Timeout value (seconds) for read/write \
                                operations.')
    parser.add_argument('--squidclientargs',
                        default='',
                        help='options for squidguard, like auth and password')
    parser.add_argument('--interval',
                        type=int,
                        default=300,
                        help='The polling interval in seconds used by icinga')
    parser.add_argument('--query',
                        required=True,
                        help="The query to run: icp-packets \
                                icp-requests icp-transfer \
                                icp-svctime requests transfer \
                                svctime syscallsdisk syscallssocket \
                                swap unlink pagefaults selectloops cpu")
    args = parser.parse_args()

    cachedStats = fetch_cached_stats(args.hostname, args.interval, args.tmpdir)

    argsList = [str(args.squidclient),
                '-h',
                str(args.hostname),
                '-p',
                str(args.port)]
    if cachedStats:
        output_stats(filter_stats(cachedStats, args.query))
    else:
        squid5min = fetch_stats(argsList)
        if not squid5min:
            for stat in stats:
                stats[stat] = "U"
        else:
            stats = parse_stats(squid5min, stats)
            cache_stats(stats, args.hostname, args.tmpdir)
        output_stats(filter_stats(stats, args.query))
