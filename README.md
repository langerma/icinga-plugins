# icinga-plugins

My icinga plugins

- cisco devices (bgp, sslsessions, waas sessions)
- jenkins jobs
- check_file_age.py which checks for the age of a file or path with different methods
- check_elasticsearch_cluster.py checking the health of elasticsearch or fire up a query

## check_jenkins_jobs.py
a script designed to get status information about jenkins jobs via API.
script is not fully finished

## cisco plugins
description is coming soon

## check_file_age.py

a plugin to check file age with different methods:

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

## check_elasticsearch_cluster.py

a plugin to check the health of an elasticsearch cluster,
you also can fire up queries and set thresholds for example: failed logins, etc.


    usage: Icinga check for elasticsearch [-h] --host HOST [--port PORT]
                                [--uri URI] [--command {health,metric}]
                                [--query QUERY] [--critical CRITICAL]
                                [--warning WARNING] [--invert]
                                [--duration DURATION]

                                optional arguments:
                    -h, --help            show this help message and exit
                    --host HOST           elasticsearch host
                    --port PORT           port that elasticsearch is running on (eg. 9200)
                    --uri URI             Uri for elasticsearch for example /elasticsearch
                    --command {health,metric}
                                        check command
                    --query QUERY         e.g: source:localhorst AND message:login failed
                    --critical CRITICAL   Critical threshold, e.g. 1, 100
                    --warning WARNING     Warning threshold, e.g. 1, 20
                    --invert              Invert the check so that an alert is triggered if the
                                          value falls below the threshold. Invert is implied if
                                          warning threshold > critical threshold
                    --duration DURATION   e.g: 1h, 15m, 32d

