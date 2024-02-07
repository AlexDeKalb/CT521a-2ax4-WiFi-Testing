#!/usr/bin/env python3
import os
import telnetlib
import re 

#Settings to create telnet session for CLI commands
host = "127.0.0.1"
port = 4001
timeout = 100
session = telnetlib.Telnet(host, port, timeout)

#This is how we will get the values to calculate the drop percentage, since there is no way to do it in a single command.

#This section gets output for packets transmitted 
null = session.read_until("default@btbits>>".encode('ascii'))
packets_transmitted = session.write("gettxpkts alex b\n".encode('ascii'))
OUTPUT = session.read_until(">>RSLT: 0".encode('ascii')) #Change :~> to what the telnet displays when finished parsing
FILE=open("output.txt", "w")
FILE.write(str(OUTPUT))
FILE.close()

#This section gets output for packets received 
null = session.read_until("default@btbits>>".encode('ascii'))
packets_received = session.write("getrxpkts alex a\n".encode('ascii'))
OUTPUT = session.read_until(">>RSLT: 0".encode('ascii')) #Change :~> to what the telnet displays when finished parsing
FILE=open("output2.txt", "w")
FILE.write(str(OUTPUT))
FILE.close()

#Using the output.txt file we will clean it up to get our txpkts 
txpkts_dirty = open("output.txt", "r")
txpkts_dirty_read = txpkts_dirty.read()
txpkts_cleaned = re.sub('\D', '', str(txpkts_dirty_read))[:-1]
packets_transmitted = txpkts_cleaned




#Using the output2.txt file we will clean it up to get our rxpkts 
rxpkts_dirty = open("output2.txt", "r")
rxpkts_dirty_read = rxpkts_dirty.read()
rxpkts_cleaned = re.sub('\D', '', str(rxpkts_dirty_read))[:-1]
packets_received = rxpkts_cleaned


#Prints out the amount of packets transmitted and the amount of packets received
print("The amount of packets transmitted is " + packets_transmitted)
print("The amount of packets received is " + packets_received)


percentage_received = (int(packets_received) / int(packets_transmitted)) * 100
percentage_dropped = 100 - percentage_received

print("The percentage of packets received by the clients is " + str(percentage_received) + "%")
print("The percentage of packets dropped by the clients is " + str(percentage_dropped) + "%")