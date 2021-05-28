#!/bin/bash
FILE='log'
total=0
regexp='^[0-9]*$'
while read line
	do
	cleanLine="echo $line | sed 's/+ /+g'"
	IFS=' ' read -ra array <<< "$cleanLine"
	for((n=10; n>=0; n--))
		do
			if [[ ${array[$n]} =~ $regexp ]]
			then
				let total=total+${array[$n]}
				break
			fi
		done
done < $FILE
echo $total

#author Max Beilin
#do not use with too big files (not more than 5-10k rows)
