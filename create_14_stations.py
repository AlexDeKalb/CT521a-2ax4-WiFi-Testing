#!/usr/bin/env python3
import os 
import telnetlib

host = "127.0.0.1"
port = 4001
timeout = 100

session = telnetlib.Telnet(host, port, timeout)
session.write("set_port 1 1 eth1 NA NA NA NA 2147483648 NA NA NA NA 16386\n".encode('ascii'))


os.system("./create_station.py --radio wiphy0 --ssid RubbleBrub-IoT --passwd testtest --security wpa2 --num_stations 7")
os.system("./create_station.py --radio wiphy1 --ssid RubbleBrub-IoT --passwd testtest --security wpa2 --num_stations 7 --start_id 0007")


