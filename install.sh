#!/bin/sh

DEST="../RPiMRE"
if [ ! -d $DEST ]
	then
		echo "Need to create dirctory"
		mkdir $DEST
		echo "Created directory: $DEST"
	else
		echo "Working directory already present"
fi

if [ -f $DEST/access.py ]
	then
		echo "Database login details in access.py preserved"
	else
		cp access.py $DEST
		echo "access.py copied into the working directory"
		echo "Update with current database login details"
fi

FILES="bmp180.py ccPowerUsage.py heatingContinuous.py heatingOneShot.py heatingToAWS.py m_temp.py PCF8574Continuous.py system_info.py \
	checkHeatingRunning.sh checkPCFRunning.sh checkPowerUsageRunning.sh"

echo ""
echo "Copying files into working directory"
for file in $FILES 
do
	echo $DEST/$file
#	diff $file $DEST/$file
	cp $file $DEST/$file
done 

echo "Files copied."
echo
echo "Crontab setup contained in the file crontab.txt"
cat crontab.txt
echo
echo "Current Crontab setting are:"
crontab -l | grep "RPiMRE"
echo
# Need to work out what libraries are used for python3.
#echo "Now installing the MySQL python libraries"
#sudo apt-get install python-mysql.connector
sudo apt-get install python3-mysqldb 
sudo apt-get install python3-smbus i2c-tools
sudo apt-get install python3-serial


#echo
echo "Install finished"

