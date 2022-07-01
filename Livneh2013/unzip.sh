#! /bin/sh

for zipfile in `ls *.bz2`
do
	echo $zipfile
	bzip2 -d $zipfile
	#rm $zipfile
done
