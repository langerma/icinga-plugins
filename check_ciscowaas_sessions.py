#!/usr/bin/python
##########################################################
#             check_ciscowaas_sessions                   #
#         (c) 2012 langer.markus@gmail.com               #
##########################################################

from optparse import OptionParser
from types import *
import sys
import os
import signal
import commands

# Process Signals
## Ignore problems when piping to head
signal.signal(signal.SIGPIPE, signal.SIG_DFL)
snmpcmd = "/usr/bin/snmpget -t 3 -v2c -Ov -c "

## Exit when control-C is pressed
def signal_handler(signal, frame):
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

class snmpSessionBaseClass(object):
	"""A Base Class For a SNMP Session"""
	def __init__(self,
				oid="sysDescr",
				Version=2,
				DestHost="localhost",
				Community="public"):

		self.oid = oid
		self.Version = Version
		self.DestHost = DestHost
		self.Community = Community
		
	def query(self):
		"""Creates SNMP query session"""
		try:
			#result = netsnmp.snmpwalk(self.oid,
			#                        Version = self.Version,
			#                        DestHost = self.DestHost,
			#                        Community = self.Community)
			cmd = snmpcmd+self.Community+" "+self.DestHost+" "+self.oid+" | cut -d ':' -f 2 | sed 's/ *//'"
			(status, output) = commands.getstatusoutput(cmd)
			if status == 0:
				if output.find("Timeout") == -1: 
					#return int(output.split()[3])
					result = (int(output),)
				else:
					print "SNMP: Timeout"
					sys.exit(3)
			else:
				print "SNMP: problem with snmpget subcommand"
				sys.exit(3)
				
		except:
			print sys.exc_info()
			result = None

		return result

# constant declaration

#oid_currentsessionstring = ".1.3.6.1.4.1.9.9.762.1.3.1.1.11"
#oid_maximumsessionstring = ".1.3.6.1.4.1.9.9.762.1.3.1.1.13"

oid_currentsessionstring = ".1.3.6.1.4.1.9.9.762.1.2.1.2.0"
oid_maximumsessionstring = ".1.3.6.1.4.1.9.9.762.1.2.1.3.0"


# variable init

current_connections = 0

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
	(options, args) = parser.parse_args()

	# Determine mode
	if options.mode == "version":
		version()

	# Check options

def check_options(parser):
	if type(options.community) == NoneType \
	or type(options.host) == NoneType:
		parser.print_usage()
		sys.exit()

if __name__ == "__main__":
        init(sys.argv[1:])
	maxcon = snmpSessionBaseClass()
	maxcon.oid = oid_maximumsessionstring
	maxcon.DestHost = options.host
	maxcon.Community = options.community
	res_tuple_maxcon = maxcon.query()
	
	curcon = snmpSessionBaseClass()
	curcon.oid = oid_currentsessionstring
	curcon.DestHost = options.host
	curcon.Community = options.community
	res_tuple_curcon = curcon.query()

	if type(res_tuple_curcon) is NoneType:
		sys.exit(3)
	else:
		for x in res_tuple_curcon:
			current_connections = current_connections + int(x)
	
		maxsessions = int(res_tuple_maxcon[0])
		warnstate = maxsessions * 0.90
		critstate = maxsessions * 0.95
	
		warnstate = int(warnstate)
		critstate = int(critstate)
	
		if current_connections < critstate and current_connections > warnstate:
			status = "WARNING"
			perfstring=" | optimized_sessions=" + str(current_connections) + ";" + str(warnstate) + ";" + str(critstate)
			print "SESSIONS " + status + " - optimized-sessions " + str(current_connections) + ";" + perfstring
			sys.exit(1)
		elif current_connections > warnstate and current_connections > critstate:
			status = "CRITCAL"
			perfstring=" | optimized_sessions=" + str(current_connections) + ";" + str(warnstate) + ";" + str(critstate)
                	print "SESSIONS " + status + " - optimized-sessions " + str(current_connections) + ";" + perfstring
			sys.exit(2)
		elif current_connections < warnstate and current_connections < critstate:
			status = "OK"
			perfstring=" | optimized_sessions=" + str(current_connections) + ";" + str(warnstate) + ";" + str(critstate)
                	print "SESSIONS " + status + " - optimized-sessions " + str(current_connections) + ";" + perfstring
			sys.exit(0)
