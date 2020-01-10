#!/usr/bin/env python
# 2020 - WeakNetLabs - Douglas Berdeaux
# Get device count using unique station MACs
# while listening for probe requests
#
from scapy.all import Dot11, sniff
import sys # for exit() and argv[]
import subprocess # to check for devices with iw

def usage():
    print "Usage: ./station_count.py (WLAN DEV)"
    sys.exit()

if len(sys.argv)<2:
    usage()
else:
    wlandev = sys.argv[1] # get device from user
    stations_list = [] # list of stations

    # check if device exists:
    # iw dev|grep wlan0mon|wc -l

    def PacketHandler(packet):
        if packet.haslayer(Dot11):
            # explanation: type 0 == mgmt frame category, subtypes are defined
            if packet.type == 0 and packet.subtype == 4: # 4 is probe request
                if packet.addr2 not in stations_list:
                    #print packet.addr2, packet.info
                    stations_list.append(packet.addr2)
        print "\r[*] Devices Found: "+str(len(stations_list)),
    sniff(iface=wlandev, prn=PacketHandler)
