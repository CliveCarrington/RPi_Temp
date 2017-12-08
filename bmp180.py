#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import logging
import Adafruit_BMP.BMP085 as BMP085

# Setup logging
logging.basicConfig(filename='/home/pi/bmp180_error.log',
  format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

# Function for storing readings into MySQL
def insertDB(temperature,pressure):

  try:

    con = mdb.connect('localhost',
                      'pi_insert',
                      'xxxxxxxxxx',
                      'measurements');
    cursor = con.cursor()

    sql = "INSERT INTO bmp180(temperature, pressure) \
    VALUES ('%s', '%s')" % \
    ( temperature, pressure)
    cursor.execute(sql)
    sql = []
    con.commit()

    con.close()

  except mdb.Error, e:
    logger.error(e)

# Get readings from sensor and store them in MySQL
sensor = BMP085.BMP085()

temperature = sensor.read_temperature()
pressure = sensor.read_sealevel_pressure(71)

insertDB(temperature,pressure)
