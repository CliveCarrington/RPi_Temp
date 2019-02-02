#!/bin/bash

#### Run the OneShot temperature capture at least once.
python ./heatingOneShot.py >> ~/log/heating.log
#### Checks whether an application is running
checkFile="heatingContinuous.py"

status=`/bin/ps -ef | grep $checkFile  | wc -l`

echo `date` "Checking $checkFile"
echo "Status = $status"

/bin/ps -ef | grep $checkFile

if [ $status -eq "1" ]
then
	echo "Need to start"
	python $checkFile >> ~/log/heating.log&

fi

