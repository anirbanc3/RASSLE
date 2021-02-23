#!/bin/bash

gcc -o ras2 ras_attack.c -w
gcc -o ecc ecc_encrypt.c -w -L/usr/local/lib -lcrypto

dec=128

for i in {1..32};	do
	var2=$dec
	hex=$(echo "obase=16; $dec"| bc);
	for j in {1..10000};	do
		(chrt -d --sched-runtime 3600 --sched-deadline 3700 --sched-period 7200 0 ./ras2 $dec $j &
		chrt -d --sched-runtime 3600 --sched-deadline 3700 --sched-period 7200 0 ./ecc $hex) 

	done
	dec=`expr $dec + 4`
done

rm ras2 ecc

echo "done"
