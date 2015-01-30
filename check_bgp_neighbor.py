#!/usr/bin/python
##########################################################
#             check_bgp_neighbor_sessions                #
#         (c) 2012 langer.markus@gmail.com               #
##########################################################

##########################################################
# i had to use system snmp command because the python libs 
# are not available on my production system...sad but true
##########################################################

from optparse import OptionParser
from types import *
import sys
import os
#import netsnmp
import signal
import commands

snmpgetcmd = "/usr/bin/snmpget -v2c -Ov -c "


#############################################################
# PLUGIN Skeleton
#############################################################
	
def version():
	print "Version: 0.1"
	sys.exit(0)

def init(argv):
	""" Used to capture all of the command line args and perform initializations"""

	# Use global namespace for flags and other major variables
	global options

	# Declarations & Variables
	usage="usage: %prog -C public -H router.example.com -n <neighbor> ..."
	parser = OptionParser(usage)

	# Handle flags
	parser.add_option("-V", "--version", dest="mode", action="store_const", const="version", help="show program's version number and exit")
	parser.add_option("-C", "", dest="community", action="store", type="string", help="Community string used for snmp")
	parser.add_option("-H", "", dest="host", action="store", type="string", help="Host to check")
        parser.add_option("-N", "", dest="bgpneighbor", action="store", type="string", help="Neighbor to check")
	(options, args) = parser.parse_args()

	# Determine mode
	if options.mode == "version":
		version()

	# Check options

def check_options(parser):
	if type(options.community) == NoneType \
	or type(options.host) == NoneType \
	or type(options.bgpneighbor) == NoneTyoe:
		parser.print_usage()
		sys.exit()

if __name__ == "__main__":
        init(sys.argv[1:])
	
	oid = ".1.3.6.1.2.1.15.3.1.2." + options.bgpneighbor
	#oid_netsnmp = netsnmp.Varbind(oid)
	cmd = snmpgetcmd+options.community+" "+options.host+" "+oid+" | cut -d ':' -f 2 | sed 's/ *//'"
	#result_bgpstatus = netsnmp.snmpget(oid_netsnmp, Version = 2, DestHost = options.host, Community = options.community)
	(status, output) = commands.getstatusoutput(cmd)
	if status == 0:
		if output.find("Timeout") == -1:
			if output.find("exists") == -1:
				#return int(output.split()[3])
				result_bgpstatus = (int(output),)
			else:
				print "SNMP: Timeout"
				sys.exit(3)
		else:
			print "SNMP: Timeout"
			sys.exit(3)
	else:
		print "SNMP: problem with snmpget subcommand"
		sys.exit(1)	



        oid = ".1.3.6.1.4.1.9.9.187.1.2.4.1.1." + options.bgpneighbor + ".1.1"
        #oid_netsnmp = netsnmp.Varbind(oid)
        cmd = snmpgetcmd+options.community+" "+options.host+" "+oid+" | cut -d ':' -f 2 | sed 's/ *//'"
	#result_bgpprefixes = netsnmp.snmpget(oid_netsnmp, Version = 2, DestHost = options.host, Community = options.community)
        (status, output) = commands.getstatusoutput(cmd)
	if status == 0:
		if output.find("Timeout") == -1:
                	#return int(output.split()[3])
                	result_bgpprefixes = (int(output),)
		else:
			print "SNMP: Timeout"
			sys.exit(3)
        else:
                print "SNMP: problem with snmpget subcommand"
                sys.exit(1)
	

	if (int(result_bgpstatus[0]) == 6) and (int(result_bgpprefixes[0]) > 10):
		status = "OK"
		perfstring=" | known_prefixes=" + str(result_bgpprefixes[0])
		print "BGP Session Status for neighbor " + options.bgpneighbor + " is " + status + " - known prefixes " + str(result_bgpprefixes[0]) + ";" + perfstring
		sys.exit(0)
	else:
		status = "CRITCAL"
               	perfstring=" | known_prefixes=" + str(result_bgpprefixes[0])
               	print "BGP Session Status for neighbor " + options.bgpneighbor + " is " + status + " - known prefixes " + str(result_bgpprefixes[0]) + ";" + perfstring
		sys.exit(2)
