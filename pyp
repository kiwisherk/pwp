#!/usr/bin/python3
#
# Make 'ip a' a little briefer
#
# I never liked the command 'ip'. I can never remember the command line arguments and the help message is too obtuse.
# Also, it is too verbose, with on interface printing five lines. This program runs the command 'ip a' and presents some
# of the information in a clearer way.

# pyp a all:          List all interfaces
#     6 ipv6          List the IPv6 addresses of the interfaces
#     m mtu           List the MTU of the interfaces.
#     e ethernet      List the Ethernet addresses of the interfaces.


import subprocess
import re
import argparse

#
# Parse the command line
#
parser = argparse.ArgumentParser(description="Make 'ip a' a litttle briefer", epilog="That's all folks!")
parser.add_argument('-a', "--all", action="store_true", help="List all interfaces")
parser.add_argument('-6', "--ipv6", action="store_true", help="List all interfaces with IPv6 addresses")
parser.add_argument('-e', "--ether", action="store_true", help="List the Ethernet addresses of the interfaces")
parser.add_argument('-m', "--mtu", action="store_true", help="List the MTU of the interfaces")
args = parser.parse_args()

allint = True if args.all else False
ipv6 = True if args.ipv6 else False
ether = True if args.ether else False
mtu = True if args.mtu else False

#
# Initialize a couple of variables
intfs = [{}]      # List of Dicts. Each dict will hold info about an interface
num_int = 0       # The number of interfaces

#
# Run the program 'ip a' and save the output in 'output
#
process = subprocess.run('ip a', shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
output = process.stdout

#
# Now interate over the output and save various bits of info about the interfaces
#
for li in output.splitlines():
        
#
# We are looking for lines that specify the interface. There is a different format between ubuntu and Mac OS. The first
# two lines are from Mac OS and the second are from Ubuntu.
#lo0: flags=8049<UP,LOOPBACK,RUNNING,MULTICAST> mtu 16384
#en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
#1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
#2: em1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq master br1 state UP group default qlen 1000
#
        # Grab the interface name (1), the flags (2), the MTU (3) and if this interface has a master
        intf_line = re.match( r'\d*[:]*\s*(\w+:) [flags=]*\d*<([\w,]+)> mtu (\d+)',li)        

        if intf_line:
             intfs.append({'name':intf_line.group(1)})
             num_int += 1            

             if intf_line.group(3):
                 intfs[num_int].update( {'MTU' : intf_line.group(3) })

             # Search the flags for PtP. This means it is a tunnel
             PtP = re.search( r'POINTOPOINT', intf_line.group(2))
             if PtP:
                 intfs[num_int].update( {'PtP' : True })

             # Master means it is slaved to a bridge
             master = re.search( r'master (\w+)',li)
             if master:
                 intfs[num_int].update( { 'master' : master.group(1)})
#
# Now look for the IPv4 address. Examples...
# 	inet 192.168.4.26/24 brd 192.168.4.255 en0
#       inet 192.168.100.1/24 brd 192.168.100.255 scope global virbr0
#
        inet = re.match( r'.+inet ([\d./]+) ', li)

        if inet:
            intfs[num_int].update( {'addr' : inet.group(1)})
#
# Now look for IPv6 address. Examples...
#	inet6 fe80::1c24:9212:5daf:90ab/64 secured scopeid 0x6
#       inet6 fe80::92e2:baff:fe14:2908/64 scope link 
            
        inet6 = re.match( r'.+inet6 ([0-9aA-fF:]+/\d+) ', li)

        if inet6:
            intfs[num_int].update( {'ipv6' : inet6.group(1)})            
#
# Get the MAC address
#	ether f0:18:98:a6:7f:fd
#       link/ether 90:e2:ba:14:29:08 brd ff:ff:ff:ff:ff:ff
#
        MAC = re.match( r'.+ether ([0-9aA-fF:]+)', li)

        if MAC:
            intfs[num_int].update( {'ether' : MAC.group(1)})

# Now delete the dummy empty dict that is first in the list. Couldn't get it to work without first creating it.
del intfs[0]

#
# Now the output loop. By default, only print the interfaces with IPv4 address, but the flags can change that or
# add additional info, such as the MTU
#
for le in intfs:

    if allint or 'addr' in le:
        print ("%-10s" % le['name'],end = ' ')

        if 'addr' in le:
            print(le['addr'], end = ' ')
    
        if ipv6 and 'ipv6' in le:
            print(le['ipv6'], end = ' ' )

        if ether and 'ether' in le:
            print(le['ether'], end = ' ')        

        if 'PtP' in le:
            print(' tunnel ', end = ' ')

        if mtu and 'MTU' in le:
            print(' MTU ', le['MTU'], end = ' ')

        if 'master' in le:
            print(' Master: ', le['master'], end = ' ')

# print a new line
        print("")
