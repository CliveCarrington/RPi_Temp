#*****************************************************
#
#	ccPowerUsage
#
#	Clive Carrington
#	Version 0.1
#	25th April 2020
#
#	History:
#		0.1. Initial version, copied from ccDataReceiver

# Definitions

logRoot = "log"

# Definitions for MySQL boolean entries (using short Int)
SQL_On = 0
SQL_Off = 1
SQL_Unk = 99

# Imports

import datetime
import sys
import serial
from heatingToAWS import sendPowerMeasurement, sendTemperature
import xml.etree.ElementTree as ET

#	Will eventually use the same source for all SQP routines!
#	from heatingToMySQL_AWS import sendHeatingData



#*********************************************************
#
#	Set of routines dealing with creating and amending the output record
#
#	constructOutputRecord creates a CSV string from the current record
#	updateField(Name, Value)
#	
#**********************************************************


def openInputChannel():

	inputHandle = serial.Serial('/dev/ttyUSB0', 57600, timeout=15)

	return inputHandle
	

# Start of Main()

# *******************************
#
#	Example of Main routine using new functions
#
#*********************************

def main_CHroutine():
	
# Open up the input channel
	inputChannel = openInputChannel()

# SET up the main loop to receive data

				
	while inputChannel.isOpen() :
		each_line = inputChannel.readline()
		if each_line != "":
			print each_line
			root = ET.fromstring(each_line)
			sensor = -1
			recordValid = False
			for child in root:
				#print(child.tag, child.text)
				if child.tag == "tmpr":
					airingCupboardTemp = child.text
				if child.tag == "sensor":
					if child.text != "0":
						break
				if child.tag == "hist":
					break
				if child.tag == "sensor" and child.text != "0":
					break	
				if child.tag == "ch1":
					#print list(child.itertext())
					houseTotal = list(child.itertext())[0]
					recordValid = True
				if child.tag == "ch3":
					solarPower = list(child.itertext())[0]
				if child.tag == "ch2":
					waterHeating = list(child.itertext())[0]
			if recordValid:
				print("Temp is {}, house is {}, solar is {} and water heating is {}."\
				.format(airingCupboardTemp, houseTotal, solarPower, waterHeating)) 
				sendPowerMeasurement(0,houseTotal, waterHeating, solarPower)
				sendTemperature("Airing Cupboard", airingCupboardTemp)
	inputchannel.close()

	return 0
	
if __name__ == '__main__':
	main_CHroutine()
