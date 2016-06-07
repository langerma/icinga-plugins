icinga-plugins
==============

My ugly icinga plugins

More to be added soon!
Sorry for the ugly code, i just did it quick and dirty to address my needs at the company. 
I am working on some cleanup and docu.

check_jenkins_jobs.py
=============
a script designed to get status information about jenkins jobs via API.
script is not fully finished

cisco plugins
==============

check_file_age.py
==============

a plugin to check file age with different methods:

usage: Icinga check for fileage [-h] --filename FILENAME [--text TEXT]
                                [--method {modified,accessed,metadata}]
                                [--warning WARNING] [--critical CRITICAL]

                                optional arguments:
                    -h, --help            show this help message and exit
                    --filename FILENAME   filename or path
                    --text TEXT           Custom Text (e.g. last modified on:)
                    --method {modified,accessed,metadata}
                                          Method what you want to check
                    --warning WARNING     Warning threshold in hours
                    --critical CRITICAL   Critical threshold in hours

