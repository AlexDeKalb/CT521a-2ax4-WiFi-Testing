#!/usr/bin/env python3
import os
import telnetlib
import time

# Settings to create telnet session for CLI commands
host = "127.0.0.1"
port = 4001
timeout = 100
session = telnetlib.Telnet(host, port, timeout)

# list of stations, will mostly likely be very helpful in the future. 
cx = ['VTsta0000-0', 'VTsta0001-0', 'VTsta0002-0', 'VTsta0003-0', 'VTsta0004-0', 'VTsta0005-0', 'VTsta0006-0',
      'VTsta0007-0', 'VTsta0008-0', 'VTsta0009-0']

# Code in the works
# These codes create test-group alex, then add all the stations to it. this is necessary for the above code to work properly
session.write("add_group alex\n".encode('ascii'))

#Adds all the CXs to the group alex 
for cxs in cx:
    write_this = "add_tgcx alex " + cxs + "\n"
    session.write(write_this.encode('ascii'))

#This code will first bring up a cx, put it in QUIESCE state, then bring up an additional station
cx_list = []
for cxs in cx:

    write_this = "set_cx_state all " + cxs + " running" + "\n"
    cx_list.append(write_this)

    for items in cx_list:
        session.write(items.encode('ascii'))
        #wait for 5 seconds 
        time.sleep(5)
    
#add_tgcx alex VTsta0000-0
#add_tgcx alex VTsta0001-0
#add_tgcx alex VTsta0002-0
#add_tgcx alex VTsta0003-0
#add_tgcx alex VTsta0004-0
#add_tgcx alex VTsta0005-0
#add_tgcx alex VTsta0006-0
#add_tgcx alex VTsta0007-0
#add_tgcx alex VTsta0008-0
#add_tgcx alex VTsta0009-0

