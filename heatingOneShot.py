#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import datetime
import MySQLdb as mdb
import logging
import smbus

#### Import dB Details from access.py
from access import hostname, username, password, dB


# DS1621 commands
START           = 0xEE
STOP            = 0x22
READ_TEMP       = 0xAA
READ_COUNTER    = 0xA8
READ_SLOPE      = 0xA9
ACCESS_CONFIG   = 0xAC
ACCESS_TH       = 0xA1
ACCESS_TL       = 0xA2

# read-only status bits
DONE      = 0x80
TH_BIT    = 0x40
TL_BIT    = 0x20
NVB       = 0x10 # Non-Volatile memory Busy

# r/w status bits (bit masks)
POL_HI    = 0x02
POL_LO    = 0xFD
ONE_SHOT  = 0x01
CONT_MODE = 0xFE
CLR_TL_TH = 0x9F

logging.basicConfig(filename='/home/pi/DS1621_error.log',
  level=logging.DEBUG,
  format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

# Load the modules (not required if they are loaded at boot) 
# os.system('modprobe w1-gpio')
# os.system('modprobe w1-therm')


# Basic numerical assist functions
def twos_comp(byte):
    '''input byte in two's complement is returned as signed integer. '''
    if len(bin(byte)[2:]) > 8:
        # shouldn't ever get here
        print '\nWarning: input ' + str(hex(byte)) + \
              ' truncated to least significant byte: ' + \
              str(hex(0xFF & byte))
        byte = 0xFF & byte
    return ~(255 - byte) if byte > 127 else byte


# Function for storing readings into MySQL
def insertDB(IDs, temperature):

  try:

    con = mdb.connect(hostname,
                      username,
                      password,
                      dB);
    cursor = con.cursor()

    for i in range(0,len(temperature)):
      sql = "INSERT INTO temperature(temperature, sensor_id) \
      VALUES ('%s', '%s')" % \
      ( temperature[i], IDs[i])
#      print sql
      cursor.execute(sql)
      sql = []
      con.commit()

    con.close()

  except mdb.Error, e:
    logger.error(e)


# routines for accessing bus data

# General read function, also updates a register

def wake_up(bus, sensor):
    ''' Device always starts in Idle mode, first reading is not usable.'''
    read_degreesC_byte(bus, sensor)
    time.sleep(0.6)

def read_degreesC_byte(bus, sensor):
    '''returns temperature in degrees Celsius as integer '''

    bus.read_byte_data(sensor, START)
    degreesC_byte = twos_comp(bus.read_byte_data(sensor, READ_TEMP))
    return degreesC_byte

def write(value, address):
	bus.write_byte_data(address,0,value)
	return -1

def read(address):
	reading = bus.read_byte(address)
	return reading

################################################
#
#      Start of "Main"
#
################################################ 

# Set up variables

address = [0x48, 0x49]
temperature = []
IDs = ["HWT_Top", "HWT_Bottom"]

# Get readings from sensors and store them in MySQL

bus = smbus.SMBus(1)
# sensorname at bus address.

for dev_addr in address:
	wake_up(bus,dev_addr)
	temp = read_degreesC_byte(bus, dev_addr)
#	print dev_addr, temp
	temperature.append(temp)

currentDT = datetime.datetime.now()
print "OneShot: ", str(currentDT), IDs, temperature
insertDB(IDs, temperature)
