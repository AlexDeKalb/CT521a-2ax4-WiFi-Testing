#!/usr/bin/env python3
import os # used to execute other python files 
import telnetlib # used to send cli commands
import re # needed for regular expressions 
import time # used for putting in pauses 
import csv #creates csv
import matplotlib.pyplot as plt #creates bar chart  
import pandas as pd #helps handle csv data to be used by matplotlib
import numpy as np #helps create a nice looking chart :) 

# Settings to create CSV header
header = ['Drop Percentage', 'Bandwidth Utilized mbps']



# Settings to create telnet session for CLI commands
host = "127.0.0.1"
port = 4001
timeout = 10000
session = telnetlib.Telnet(host, port, timeout)

# Global variables for drop percentage and bandwidth 
current_drop_percentage = "Placeholder"
#current_bandwidth_usage = 0 # Commenting out because I don't believe this needs to be here atm. 

# Creating our function which will be used to calculate drop percentage 
def calculate_drop_percentage():


    # This is how we will get the values to calculate the drop percentage, since there is no way to do it in a single command.

    # This section gets output for packets transmitted
    null = session.read_until("default@btbits>>".encode('ascii'))
    packets_transmitted = session.write("gettxpkts alex b\n".encode('ascii'))
    OUTPUT = session.read_until(
        ">>RSLT: 0".encode('ascii'))  # Change :~> to what the telnet displays when finished parsing
    FILE = open("output.txt", "w")
    FILE.write(str(OUTPUT))
    FILE.close()

    # This section gets output for packets received
    null = session.read_until("default@btbits>>".encode('ascii'))
    packets_received = session.write("getrxpkts alex a\n".encode('ascii'))
    OUTPUT = session.read_until(
        ">>RSLT: 0".encode('ascii'))  # Change :~> to what the telnet displays when finished parsing
    FILE = open("output2.txt", "w")
    FILE.write(str(OUTPUT))
    FILE.close()

    # Using the output.txt file we will clean it up to get our txpkts
    txpkts_dirty = open("output.txt", "r")
    txpkts_dirty_read = txpkts_dirty.read()
    txpkts_cleaned = re.sub('\D', '', str(txpkts_dirty_read))[:-1]
    packets_transmitted = txpkts_cleaned

    # Using the output2.txt file we will clean it up to get our rxpkts
    rxpkts_dirty = open("output2.txt", "r")
    rxpkts_dirty_read = rxpkts_dirty.read()
    rxpkts_cleaned = re.sub('\D', '', str(rxpkts_dirty_read))[:-1]
    packets_received = rxpkts_cleaned

    # Prints out the amount of packets transmitted and the amount of packets received
    file_object = open('drop_percentage.txt', 'a')
    #findings1 = "The amount of packets transmitted is " + packets_transmitted
    print("The amount of packets transmitted is " + packets_transmitted)
    #findings2 = "The amount of packets received is " + packets_received
    print("The amount of packets received is " + packets_received)
    percentage_received = (int(packets_received) / int(packets_transmitted)) * 100
    percentage_dropped = 100 - percentage_received
    
    
    #findings3 = "The percentage of packets received by the clients is " + str(percentage_received) + "%"
    print("The percentage of packets received by the clients is " + str(percentage_received) + "%")

    # Get the drop percentage, which will then be logged to csv file to make a chart
    global current_drop_percentage
    Drop_Percentage_rounded = round(percentage_dropped, 2)
    Drop_Percentage = str(Drop_Percentage_rounded)
    current_drop_percentage = Drop_Percentage
    print("The percentage of packets dropped by the clients is " + str(percentage_dropped) + "%")
    #file_object.write(findings1 + "\n")
    #file_object.write(findings2 + "\n")
    #file_object.write(findings3 + "\n")
    #file_object.write(findings4 + "\n")
    #file_object.close()

    








# This is to loop through the script 10 times, each time making a new script. 
for numbers in range(10):
    #these blank lists and index are used to Iterate slowly in the for loops.
    cx_list = []
    cx_total = []
    index = 1
    
    # Creates the test group "alex" 
    session.write("add_group alex\n".encode('ascii'))


    
    # list of stations, will mostly likely be very helpful in the future. 
    cx = ['VTsta0000-0', 'VTsta0001-0', 'VTsta0002-0', 'VTsta0003-0', 'VTsta0004-0', 'VTsta0005-0', 'VTsta0006-0',
          'VTsta0007-0', 'VTsta0008-0', 'VTsta0009-0', 'VTsta0010-0', 'VTsta0011-0', 'VTsta0012-0', 'VTsta0013-0']

    # Adds all the CXs to the group alex 
    for cxs in cx:
        write_this = "add_tgcx alex " + cxs + "\n"
        session.write(write_this.encode('ascii'))
    
    # List of the station's bandwidths, this will be used to create a chart. 
    cx_bandwidth = [20, 20, 10, 10, 10, 30, 10, 50, 5, 5, 50, 10, 10, 10]


    # Resets the counters on all the stations 
    session.write("clear_cx_counters\n".encode('ascii'))
    
    # Creates or overwrites DropPercentageAndBandwidth.csv 
    with open('DropPercentageAndBandwidth.csv', 'w', newline = '') as f:
        # write the header
        writer = csv.writer(f)
        writer.writerow(header)

    #This code will first bring up a cx, put it in QUIESCE state, take a drop_percentage reading, then bring up an additional cx
    # until all the cxs have been started and a drop percentage taken while they are in QUIESCE state. 
    for cxs in cx:

        write_this = "set_cx_state all " + cxs + " running" + "\n"
        cx_list.append(write_this)

        for items in cx_list:
            print(items)    
            session.write(items.encode('ascii'))
            
        print("60 second sleep to allow CXs to run")   
        time.sleep(5) #wait for 30 seconds  
        #session.close()
        #session = telnetlib.Telnet(host, port, timeout)
        session.read_until("default@btbits>>".encode('ascii'))
        session.write("set_cx_state all all quiesce\n".encode('ascii'))
        print("set_cx_state all all quiesce")
        print("Waiting for 15 seconds for quiesce state then calculating the drop percentage")
        time.sleep(10) #wait for 15 seconds 
        #session.read_all()
        #session.write("set_cx_state all all quiesce\n".encode('ascii'))
        #print("set_cx_state all all quiesce 2nd attempt")
        session.close()
        session = telnetlib.Telnet(host, port, timeout)
        #time.sleep(15) #wait for 15 seconds 
        calculate_drop_percentage()
        current_total = sum(cx_bandwidth[0:index])
        current_bandwidth_usage = str(current_total)
        f = open('DropPercentageAndBandwidth.csv', 'a', newline = '')
        data = [current_drop_percentage, current_bandwidth_usage]
        print(data)
        writer = csv.writer(f)
        writer.writerow(data)
        f.close()
        index += 1


    # Initialize the lists for X and Y in barchart

    data = pd.read_csv('DropPercentageAndBandwidth.csv')
    df = pd.DataFrame(data)
    dropped = list(df.iloc[:, 0])
    bandwidth_mbps = list(df.iloc[:, 1])
    # Plot the data using bar() method
    x = np.arange(len(bandwidth_mbps)) # the label locations
    width = .3 # the width of the bars
    fig, ax = plt.subplots()
    ax.set_xlabel('Bandwidth(in Mbps)')
    ax.set_title('Drop Percentage as Bandwidth increases')
    ax.set_ylabel('Drop %')
    ax.set_xticks(x)
    ax.set_xticklabels(bandwidth_mbps)

    pps = ax.bar(x - width/2, dropped, width, label='Drop %')
    for p in pps:
       height = p.get_height()
       ax.annotate('{}'.format(height),
          xy=(p.get_x() + p.get_width() / 2, height),
          xytext=(0, 3), # 3 points vertical offset
          textcoords="offset points",
          ha='center', va='bottom')


    filename = "DropTest_WiFi5_U6Lite_" + str(numbers + 1)
    plt.savefig(filename)