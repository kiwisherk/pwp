# pwp
A briefer 'ip a' command
I never liked the command 'ip'. I can never remember the command line arguments and the help message is too obtuse.      
Also, it is too verbose, with on interface printing five lines. This program runs the command 'ip a' and presents some   
of the information in a clearer way.                                                                                     

usage: pyp [-h] [-a] [-6] [-e] [-m]

Make 'ip a' a litttle briefer

optional arguments:
  -h, --help   show this help message and exit
  -a, --all    List all interfaces
  -6, --ipv6   List all interfaces with IPv6 addresses
  -e, --ether  List the Ethernet addresses of the interfaces
  -m, --mtu    List the MTU of the interfaces

That's all folks!
