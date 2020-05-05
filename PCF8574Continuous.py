#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import datetime
import MySQLdb as mdb
import logging
import smbus
from heatingToAWS import sendHeatingData
#### Import dB Details from access.py
from access import hostname, username, password, dB

# PCF8574 commands
PCF8574		= 0x20

logging.basicConfig(filename='/home/pi/PCF8574_error.log',
  level=logging.DEBUG,
  format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

# General read function, also updates a register

def write(address, value):
	try:
		bus.write_byte(address,value)
	except IOError as io_err:
		logger.error(io_err)
		print(io_err)
	return -1

def read(address):
	try:
		reading = bus.read_byte(address)
	except IOError as io_err:
		logger.error(io_err)
		print(io_err)
	return reading

################################################
#
#      Start of "Main"
#
################################################ 

# Set up variables

# Get readings from sensors and store them in MySQL

bus = smbus.SMBus(1)

write(PCF8574, 0xFF)

while 1:
	try:
		pins = read(PCF8574)
		print "%02x" % pins
#		print pins
#			As the most significant two bits are unconnected,
#			they should always be high. Hence, if the value of 
#			the pins is less than 192 (C0) we need to reset.
		if (pins < 0xC0):
			print "Resetting to FF"
			write(PCF8574, 0xFF)
		else:
			sendHeatingData(pins)
	except IOError as io_error:
		print("bus Read error", io_error)
		print "Clash"		
	time.sleep(20)

