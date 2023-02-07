#!bin/bash

while true
do
	echo "Start Request!"
	scp a19root@cpen291-19.ece.ubc.ca:/home/a19root/target.png "C:\Users\thoma\Desktop\ML\ToBePredicted" 
	echo "Finish Request!"
	echo "Start Result!"
	scp "C:/Users/thoma/Desktop/ML/pred_result.txt" a19root@cpen291-19.ece.ubc.ca:
	echo "Finish Result!"
	sleep 2
done