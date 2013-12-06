#!/usr/bin/env python

#****************************************************************************
#*   DS18B20 To Graphite                                                    *
#*   Log data from DS18B20 sensors to graphite                              *
#*                                                                          *
#*   Copyright (C) 2013 by Jeremy Falling except where noted.               *
#*                                                                          *
#*   This program is free software: you can redistribute it and/or modify   *
#*   it under the terms of the GNU General Public License as published by   *
#*   the Free Software Foundation, either version 3 of the License, or      *
#*   (at your option) any later version.                                    *
#*                                                                          *
#*   This program is distributed in the hope that it will be useful,        *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of         *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          *
#*   GNU General Public License for more details.                           *
#*                                                                          *
#*   You should have received a copy of the GNU General Public License      *
#*   along with this program.  If not, see <http://www.gnu.org/licenses/>.  *
#****************************************************************************



import sys
import time
import os
import platform
import subprocess
from socket import socket
import re

#change this to your carbon server and port
CARBON_SERVER = '10.10.0.5'
CARBON_PORT = 2003

#28-00000504c4ca  near pi
#28-000005056497  radiator
#28-000005059702  wall
#28-0000050542cc  below window
#28-00000505ba75  next to servers


delay = 20
if len(sys.argv) > 1:
  delay = int( sys.argv[1] )

#run forever
while True:
        #get the sensor ids into an array
        w1Slaves = open("/sys/devices/w1_bus_master1/w1_master_slaves", "r")
        listOfSensors = w1Slaves.read().splitlines()
        w1Slaves.close()

        i = 0
        sensorData = []
        for sensor in listOfSensors:
                crc = '';
                #ensure we get valid data (crc must = yes)
                while crc.split("\n")[0].find("YES") == -1:
                        currentSensor = open("/sys/devices/w1_bus_master1/%(sensor)s/w1_slave" % locals(), "r")
                        data=currentSensor.readlines()
                        currentSensor.close()

                        #split the two lines into two variables
                        crc=data[0]
                        temp=data[1]

                        currentReading = re.search(r't=.\d*', "%(temp)s" % locals())
                        i+1

                        #convert to a reasonable number, ie 12.02
                        sensorData.append((float(currentReading.group().replace('t=','')))* .001)


        sock = socket()
        try:
          sock.connect( (CARBON_SERVER,CARBON_PORT) )
        except:
          print "Couldn't connect to %(server)s on port %(port)d, is carbon-agent.py running?" % { 'server':CARBON_SERVER, 'port':CARBON_PORT }
          sys.exit(1)

        now = int( time.time() )
        lines = []
        i = 0
        for sensor in listOfSensors:
                lines.append("%s %s %d" % (sensor,sensorData[i],now))
                i=i+1


        message = '\n'.join(lines) + '\n' #all lines must end in a newline
        print "sending message\n"
        print '-' * 80
        print message
        print
        sock.sendall(message)

        time.sleep(delay)
