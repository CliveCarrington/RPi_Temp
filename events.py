#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import the python libraries
import RPi.GPIO as GPIO
import logging
import MySQLdb as mdb
import time

logging.basicConfig(filename='/home/event_error.log',
  level=logging.DEBUG,
  format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

# Function called when GPIO.RISING
def storeFunction(channel):
  print("Signal detected")

  con = mdb.connect('localhost', \
                    'pi_insert', \
                    'pi_insert', \
                    'measurements');

  try:
    cur = con.cursor()
    cur.execute("""INSERT INTO events(event) VALUES(%s)""", ('catflap'))
    con.commit()

  except mdb.Error, e:
    logger.error(e)

  finally:
    if con:
      con.close()

print "Sensor event monitoring (CTRL-C to exit)"

# use the BCM GPIO numbering
GPIO.setmode(GPIO.BCM)

# Definie the BCM-PIN number
GPIO_PIR = 2

# Define pin as input with standard high signaal
GPIO.setup(GPIO_PIR, GPIO.IN, pull_up_down = GPIO.PUD_UP)

try:
  # Loop while true = true
  while True :

    # Wait for the trigger then call the function
    GPIO.wait_for_edge(GPIO_PIR, GPIO.RISING)
    storeFunction(2)
    time.sleep(1)

except KeyboardInterrupt:
  # Reset the GPIO settings
  GPIO.cleanup()
