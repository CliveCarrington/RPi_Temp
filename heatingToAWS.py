#!/usr/bin/python
# -*- coding: utf-8 -*-


#import os
#import glob
import time
import MySQLdb as mdb
import sys
import logging
#### Import dB Details from access.py
from access import hostname, username, password, dB

##############################################
#
#  Heating Controls variables
#
##############################################
logging.basicConfig(filename='/home/pi/log/heating_error.log',
  level=logging.DEBUG,
  format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

# Set constants for the Raw data
BIT_NOT_CH      = 0x01
BIT_CH          = 0x02
BIT_ROOM        = 0x04
BIT_HW          = 0x08
BIT_NOT_HW      = 0x10
BIT_BOILER      = 0x20

# Set values for entering the data into the database. Needed a mechanism to show a "Maybe", when value unknown

ON      = 2
OFF     = 0
MAYBE   = 1

def sendHeatingData(raw):
        if raw < 0xC0:          # First check whether this is a false reading
                return
        # creat boolean values for each bit
        NOT_CH  = not raw & BIT_NOT_CH
        CH      = not raw & BIT_CH
        ROOM    = not raw & BIT_ROOM
        HW      = not raw & BIT_HW
        NOT_HW  = not raw & BIT_NOT_HW
        BOILER  = not raw & BIT_BOILER

#       Set all values to Maybe, so that we can tell missing data

        sqlBOILER       = MAYBE
        sqlHW           = MAYBE
        sqlROOMSTATON   = MAYBE
        sqlWATERSTATON  = MAYBE
        sqlCH           = MAYBE

        print 'Assessing raw: %.2X' % raw
        if BOILER:              # Boiler on
                print "Boiler on"
                sqlBOILER = ON
        else:
                sqlBOILER = OFF

        if NOT_CH:
                print "CH off"
                sqlCH = OFF
        else:
                print "CH on"
                sqlCH = ON
        if not HW:
                print "HW off. Tank Stat off"
                sqlHW = OFF
                sqlWATERSTATON = ON
        else:
                if NOT_HW:
                        print "Tank stat warm, maybe want HW"
                        sqlWATERSTATON = OFF
                else:
                        print "HW on, tank stat cold"
                        sqlHW = ON
                        sqlWATERSTATON = ON
        if CH and ROOM:
                print "Room stat cold"
                sqlROOMSTATON = ON
        if CH and not ROOM:
                print "Room Stat hot"
                sqlROOMSTATON = OFF

        print "CH = ",sqlCH
        print "HW = ",sqlHW
        print "Room stat = ",sqlROOMSTATON
        print "Tank Stat = ",sqlWATERSTATON
        print "Boiler Status = ",sqlBOILER

        try:
                con = mdb.connect(hostname, username, password, dB)
                cur = con.cursor()
		cur.execute("""INSERT INTO centralHeating( rawReading, askForHeating, \
			askForHotWater, roomStatOn, tankStatOn, boilerOn ) \
			VALUES(%s , %s, %s, %s, %s, %s )""", \
			(raw, sqlCH, sqlHW, sqlROOMSTATON, sqlWATERSTATON, sqlBOILER))
                con.commit()
        except mdb.Error, e:
                #con.rollback()
                print "Error %d: %s" % (e.args[0],e.args[1])
                #sys.exit(1)
  #	except:
  #  		print("Error in sendHeatingData")
#	print(Hello)

def sendHeatingData_old (rawReading):
        try:
                con = mdb.connect(hostname, username, password, dB)
                cur = con.cursor()
                cur.execute("""INSERT INTO centralHeating(rawReading, roomTemperature)
                        VALUES(%s, %s )""", (rawReading, "20"))
                con.commit()
        except mdb.Error, e:
                #con.rollback()
                print "Error %d: %s" % (e.args[0],e.args[1])
                #sys.exit(1)
  	except:
    		print("Error in sendHeatingData")
#	print(Hello)

# Function for storing readings into MySQL
def sendTemperature(tempID, temperature):

  try:

    con = mdb.connect(hostname,
                      username,
                      password,
                      dB);
    cursor = con.cursor()

    sql = "INSERT INTO temperature(temperature, sensor_ID) \
            VALUES ('%s', '%s')" % \
            ( temperature, tempID)
    cursor.execute(sql)
    con.commit()

    con.close()

  except mdb.Error, e:
    logger.error(e)
    print("Error in sendTemperature")
  except:
    print("Error in sendTemperature")


def sendPowerMeasurement(dtg, houseTotal, waterHeating, solarPower):
        try:
                con = mdb.connect(hostname, username, password, dB)
                cur = con.cursor()
                cur.execute("""INSERT INTO powerReadings(houseTotal, waterHeating, solarPower)
                        VALUES(%s, %s, %s )""", (houseTotal, waterHeating, solarPower))
                con.commit()
		#print("Sent ", houseTotal)
        except mdb.Error, e:
                #con.rollback()
                print "Error %d: %s" % (e.args[0],e.args[1])
                #sys.exit(1)
	except:
    		print("Error in sendPowerMeasurement")

#def sendHeatingDataOld (recordDate, roomTemp, topTankTemp, bottomTankTemp, \
#						askForHeating, askForHotWater, roomStatOn, tankStatOn, boilerOn, \
#						solarPower, houseTotal, waterHeating ):
# """ Function doc. Send all data into main centralHeating table """	
#	try:
#		con = mdb.connect('192.168.1.13', 'pi_insert', 'xxxxxxxx', 'xxxxxxxxx')
#		cur = con.cursor()
#		if recordDate == 0:
#			cur.execute("""INSERT INTO centralHeating(tempRoom, tempTopTank, tempBottomTank, askForHeating, \
#			askForHotWater, roomStatOn, tankStatOn, boilerOn, solarPower, houseTotal, waterHeating ) \
#			VALUES(%s , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )""", \
#			(roomTemp, topTankTemp, bottomTankTemp, askForHeating, askForHotWater, roomStatOn, tankStatOn, boilerOn, solarPower, houseTotal, waterHeating ))
#		else:
#			cur.execute("""INSERT INTO centralHeating(dtg, tempRoom, tempTopTank, tempBottomTank, askForHeating, \
#			askForHotWater, roomStatOn, tankStatOn, boilerOn, solarPower, houseTotal, waterHeating ) \
#			VALUES(%s, %s , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )""", \
#			(recordDate, roomTemp, topTankTemp, bottomTankTemp, askForHeating, askForHotWater, roomStatOn, tankStatOn, boilerOn, solarPower, houseTotal, waterHeating))
#		con.commit()		
#	except mdb.Error, e:
#		#con.rollback()
#		print "Error %d: %s" % (e.args[0],e.args[1])
#		sys.exit(1)
#	sendPowerMeasurement(0, houseTotal, waterHeating, solarPower)


#sendPowerMeasurement(0, 1, 2, 3)
 
