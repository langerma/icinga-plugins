icinga-plugins
=========================
My icinga plugins

- cisco devices (bgp, sslsessions, waas sessions)
- jenkins jobs
- check_file_age.py which checks for the age of a file or path with different methods
- check_elasticsearch_cluster.py checking the health of elasticsearch or fire up a query
- check_squid.py check different metrics from squid.

check_jenkins_jobs.py
-------------------------
a script designed to get status information about jenkins jobs via API.
script is not fully finished

cisco plugins
-------------------------
description is coming soon
as of writing this I am going to migrate to argparse and move away from the command lib.

check_file_age.py
-------------------------
a plugin to check file age with different methods:

```
    usage: Icinga check for fileage [-h] --filename FILENAME
                                [--method {modified,accessed,metadata}]
                                [--warning WARNING] [--critical CRITICAL]

                                optional arguments:
                    -h, --help            show this help message and exit
                    --filename FILENAME   filename or path
                    --method {modified,accessed,metadata}
                                          Method what you want to check
                    --warning WARNING     Warning threshold in hours
                    --critical CRITICAL   Critical threshold in hours
```
check_elasticsearch_cluster.py
-------------------------
a plugin to check the health of an elasticsearch cluster,
you also can fire up queries and set thresholds for example: failed logins, etc.

```
    usage: Icinga check for elasticsearch [-h] --host HOST [--port PORT]
                                [--uri URI] [--command {health,metric}]
                                [--index INDEX] [--query QUERY]
                                [--critical CRITICAL]
                                [--warning WARNING] [--invert]
                                [--duration DURATION] [--top TOP]
                                [--field FIELD]

                                optional arguments:
                    -h, --help            show this help message and exit
                    --host HOST           elasticsearch host
                    --port PORT           port that elasticsearch is running on (eg. 9200)
                    --ssl                 Connect using HTTPS
                    --ssl-insecure        Do not verify HTTPS cert
                    --ssl-cert SSL-CERT   client cert for HTTPS auth
                    --ssl-key  SSL-KEY    client key for HTTPS auth
                    --uri URI             Uri for elasticsearch for example /elasticsearch
                    --command {health,metric}
                                        check command
                    --index INDEX         the index you want to query for example logstash-*
                    --query QUERY         e.g: source:localhorst AND message:login failed
                    --critical CRITICAL   Critical threshold, e.g. 1, 100
                    --warning WARNING     Warning threshold, e.g. 1, 20
                    --invert              Invert the check so that an alert is triggered if the
                                          value falls below the threshold. Invert is implied if
                                          warning threshold > critical threshold
                    --duration DURATION   e.g: 1h, 15m, 32d
                    --top TOP             display top hits for query
                    --field FIELD         Name of the field you want to have in your top analysis
```
check_squid.py
-------------------------
a plugin to check different metrics from squid proxy server over squid client.
i want do get rid of squidclient and implement that in pure python to not have a dependencie.

```
    usage: Icinga check for Squid Proxy Server [-h] [--squidclient SQUIDCLIENT]
                                [--tmpdir TMPDIR]
                                [--hostname HOSTNAME] [--bind BIND]
                                [--port PORT] [--timeout TIMEOUT]
                                [--squidclientargs SQUIDCLIENTARGS]
                                [--interval INTERVAL] --query QUERY

                                optional arguments:
                    -h, --help            show this help message and exit
                    --squidclient SQUIDCLIENT
                                          path to squidclient
                    --tmpdir TMPDIR       temporary file dir
                    --hostname HOSTNAME   Retrieve URL from cache on hostname. Default is
                                          localhost.
                    --bind BIND           Specify a local IP address to bind to. Default is
                                          none.
                    --port PORT           Port number of cache. Default is 3128.
                    --timeout TIMEOUT     Timeout value (seconds) for read/write operations.
                    --squidclientargs SQUIDCLIENTARGS
                                          options for squidguard, like auth and password
                    --interval INTERVAL   The polling interval in seconds used by icinga
                    --query QUERY         The query to run: icp-packets icp-requests icp-
                                          transfer icp-svctime requests transfer svctime
                                          syscallsdisk syscallssocket swap unlink pagefaults
                                          selectloops cpu
```
check_oracle_cellcli.py
--------------------------
you can check different metrics on oracle storagecell servers

```
    usage: Icinga check for cellcli [-h] [--dcli DCLI] [--hostname HOSTNAME]
                                [--username USERNAME] [--query QUERY]
                                [--warning WARNING] [--critical CRITICAL]

                                optional arguments:
                    -h, --help           show this help message and exit
                    --dcli DCLI          path to dcli. /bin/dcli
                    --hostname HOSTNAME  Cell hostname
                    --username USERNAME  username for the cellcli connection
                    --query QUERY        The query to run: cellcli -e list metriccurrent
                                         CD_IO_UTIL
                    --warning WARNING    warning threshold: default=90
                    --critical CRITICAL  critical threshold: default=95
```
check_oracle_rdsinfo.py
--------------------------
check the counters of rds-info on solaris

```
    usage: Icinga check for rds-info [-h] [--rdsinfo RDSINFO] --metric METRIC
                                --warning WARNING --critical CRITICAL

                                optional arguments:
                    -h, --help           show this help message and exit
                    --rdsinfo RDSINFO    path to rds-info. /usr/bin/rdsinfo
                    --metric METRIC      metric you want to check e.g: send_queue_full or
                                         ib_tx_ring_full
                    --warning WARNING    warning threshold
                    --critical CRITICAL  critical threshold
```

