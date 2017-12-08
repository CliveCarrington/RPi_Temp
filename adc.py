#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import logging
from Adafruit_ADS1x15 import ADS1x15

# Setup logging
logging.basicConfig(filename='/home/pi/adc_error.log',
  format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

# Function for storing readings into MySQL
def insertDB(level):

  try:

    con = mdb.connect('localhost',
                      'pi_insert',
                      'xxxxxxxxxx',
                      'measurements');
    cursor = con.cursor()

    sql = "INSERT INTO light(level) \
    VALUES ('%s')" % \
    (level)
    cursor.execute(sql)
    sql = []
    con.commit()

    con.close()

  except mdb.Error, e:
    logger.error(e)

# Get readings from sensor and store them in MySQL

ADS1015 = 0x00  # 12-bit ADC
gain = 4096     # +/- 4.096V
sps = 250       # 250 samples per second

# Initialise the ADC
adc = ADS1x15(ic=ADS1015)

# Read channel 0 in single-ended mode using the settings above
level = adc.readADCSingleEnded(0, gain, sps) / 1000

insertDB(level)
