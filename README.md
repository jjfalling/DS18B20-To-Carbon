DS18B20-To-Carbon
===================

Log data from DS18B20 sensors to carbon using a Raspberry Pi.

This script will gather the sensor values for each DS18B20 attached to your pi and put the data into graphite using the serial number of each sensor.

This script gets a list of sensors each run so there is no need to restart it after adding or removing sensors from the bus. 


Tested on raspbian and xbian with python 2.7.3
