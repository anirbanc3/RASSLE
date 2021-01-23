#!/bin/bash

gcc -o ras2 trial_2.c -w
gcc -o ecc ecc_encrypt.c -w -lcrypto

counter=0

input="sample_nonces.txt"
while IFS= read -r line
do
 	echo "$line"
	chrt -d --sched-runtime 3600 --sched-deadline 3700 --sched-period 7200 0 ./ras2 tst $counter &
	chrt -d --sched-runtime 3600 --sched-deadline 3700 --sched-period 7200 0 ./ecc $line
	((counter++))
done < "$input"

rm ras2 ecc

echo "done"
