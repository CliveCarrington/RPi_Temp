#!/usr/bin/python
# -*- coding: utf-8 -*-


#import os
#import glob
import time
import MySQLdb as mdb
import sys
#### Import dB Details from access.py
from access import hostname, username, password, dB

def sendHeatingData (rawReading):
        try:
                con = mdb.connect(hostname, username, password, dB)
                cur = con.cursor()
                cur.execute("""INSERT INTO centralHeating(rawReading, roomTemperature)
                        VALUES(%s, %s )""", (rawReading, "20"))
                con.commit()
        except mdb.Error, e:
                #con.rollback()
                print "Error %d: %s" % (e.args[0],e.args[1])
                sys.exit(1)
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
                sys.exit(1)


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
 
