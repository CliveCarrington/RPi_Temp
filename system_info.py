#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import os
import sys
import MySQLdb as mdb

#### Import dB Details from access.py
from access import hostname, username, password, dB, systemName


# Function for storing readings into MySQL
def insertDB(system_load, ram, disk, temperature):

  try:
    con = mdb.connect(hostname,
                      username,
                      password,
                      dB);
    cursor = con.cursor()

    sql = "INSERT INTO system_info(`systemName`, `load`,`ram`,`disk`,`temperature`) \
    VALUES ('%s', '%s', '%s', '%s', '%s')" % \
    (systemName, system_load, ram, disk, temperature)
    cursor.execute(sql)
    con.commit()

    con.close()

  except mdb.Error:
    e = sys.exc_info()[0]
    con.rollback()
    print( "Error" , e.args[0] , e.args[1])
    sys.exit(1)

# returns the system load over the past minute
def get_load():
    try:
        s = subprocess.check_output(["cat","/proc/loadavg"])
        return float(s.split()[0])
    except:
        return 0
        e = sys.exc_info()[0]
        con.rollback()
        print( "Error" , e.args[0] , e.args[1])

# Returns the used ram as a percentage of the total available
def get_ram():
    try:
        s = subprocess.check_output(["free","-m"])
	# Need to convert to a string, rather than a bytes object
        s_string = s.decode('utf-8')
        lines = s_string.split("\n")
        used_mem = float(lines[1].split()[2])
        total_mem = float(lines[1].split()[1])
#        print("Total Mem", total_mem, "Used Mem", used_mem)
        return (int((used_mem/total_mem)*100))
    except:
        e = sys.exc_info()[0]
        con.rollback()
        print( "Error" , e.args[0] , e.args[1])
        return 0

# Returns the percentage used disk space on the /dev/root partition
def get_disk():
    try:
        s = subprocess.check_output(["df","/"])
        s_string = s.decode('utf-8')
        lines = s_string.split("\n")
        return int(lines[1].split("%")[0].split()[4])
    except:
        return 0
        e = sys.exc_info()[0]
        con.rollback()
        print( "Error" , e.args[0] , e.args[1])

# Returns the temperature in degrees C of the CPU
def get_temperature():
    try:
        # The dir_path is no longer valid, but vcgencmd is in /usr/bin, so can use directly
        #dir_path="/opt/vc/bin/vcgencmd"
        s = subprocess.check_output(["vcgencmd","measure_temp"])
        s_string = s.decode('utf-8')
        return float(s_string.split("=")[1][:-3])
    except:
        e = sys.exc_info()[0]
        con.rollback()
        print( "Error" , e.args[0] , e.args[1])
        return 0

got_load = str(get_load())
got_ram = str(get_ram())
got_disk = str(get_disk())
got_temperature = str(get_temperature())

insertDB(got_load, got_ram, got_disk, got_temperature)
