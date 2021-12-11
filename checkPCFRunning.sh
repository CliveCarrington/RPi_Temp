#!/bin/bash

checkFile="PCF8574Continuous.py"
logFile="/home/pi/log/PCF8574_log.txt"
#### Run the OneShot temperature capture at least once.
# Decided that, currently, PCF8574 outputs details once every 20 seconds, that we don't need a oneshot like the temperature recorder
# python ./PCF8574OneShot.py >> $logFile
#### Checks whether an application is running
status=`/bin/ps -ef | grep $checkFile  | wc -l`

echo `date` "Checking $checkFile"
echo "Status = $status"

/bin/ps -ef | grep $checkFile

if [ $status -eq "1" ]
then
	echo "Need to start"
	echo $logFile
	echo $checkFile
	python $checkFile >> $logFile &

fi

