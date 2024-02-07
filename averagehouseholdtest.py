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
os.system("./create_l3.py --endp_a 'sta0000' --endp_b 'eth1' --min_rate_a '56000' --min_rate_b '20000000'")
os.system("./create_l3.py --endp_a 'sta0001' --endp_b 'eth1' --min_rate_a '56000' --min_rate_b '20000000'")
os.system("./create_l3.py --endp_a 'sta0002' --endp_b 'eth1' --min_rate_a '56000' --min_rate_b '10000000'")
os.system("./create_l3.py --endp_a 'sta0003' --endp_b 'eth1' --min_rate_a '56000' --min_rate_b '10000000'")
os.system("./create_l3.py --endp_a 'sta0004' --endp_b 'eth1' --min_rate_a '56000' --min_rate_b '10000000'")
os.system("./create_l3.py --endp_a 'sta0005' --endp_b 'eth1' --min_rate_a '56000' --min_rate_b '30000000'")
os.system("./create_l3.py --endp_a 'sta0006' --endp_b 'eth1' --min_rate_a '56000' --min_rate_b '10000000'")
os.system("./create_l3.py --endp_a 'sta0007' --endp_b 'eth1' --min_rate_a '56000' --min_rate_b '50000000'")
os.system("./create_l3.py --endp_a 'sta0008' --endp_b 'eth1' --min_rate_a '56000' --min_rate_b '5000000'")
os.system("./create_l3.py --endp_a 'sta0009' --endp_b 'eth1' --min_rate_a '56000' --min_rate_b '5000000'")
os.system("./create_l3.py --endp_a 'sta0010' --endp_b 'eth1' --min_rate_a '56000' --min_rate_b '50000000'")
os.system("./create_l3.py --endp_a 'sta0011' --endp_b 'eth1' --min_rate_a '56000' --min_rate_b '10000000'")
os.system("./create_l3.py --endp_a 'sta0012' --endp_b 'eth1' --min_rate_a '56000' --min_rate_b '10000000'")
os.system("./create_l3.py --endp_a 'sta0013' --endp_b 'eth1' --min_rate_a '56000' --min_rate_b '10000000'")