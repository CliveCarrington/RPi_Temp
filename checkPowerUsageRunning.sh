#!/bin/bash

checkFile="ccPowerUsage.py"
logFile="/home/pi/log/powerUsage.txt"

#### Checks whether an application is running
status=`/bin/ps -ef | grep $checkFile  | wc -l`

echo `date` "Checking $checkFile"
echo "Status = $status"

/bin/ps -ef | grep $checkFile

if [ $status -eq "1" ]
then
	echo "Need to start"
	python $checkFile >> $logFile &

fi

