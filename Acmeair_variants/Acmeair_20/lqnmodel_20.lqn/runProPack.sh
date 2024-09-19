#!/bin/sh
ms=("MSauthEntry" "MSvalidateidEntry" "MSviewprofileEntry" "MSupdateprofileEntry" "MSupdateMilesEntry"
            "MSbookflightsEntry" "MScancelbookingEntry" "MSqueryflightsEntry" "MSgetrewardmilesEntry")

echo  "name,ncopt,ntopt" > "ProPackSol.csv"
for w in ${ms[@]}; do
	dataname="./ProPackProfile/$w.csv"
	echo $dataname
	res=$(python3 /Users/emilio-imt/git/Wless/ProPack/propack.py -datafile $dataname|grep -e "Multi-objective sol")
	proPackConc=$(echo "$res" | grep  -o -E "[0-9]+")
	echo "$w,$proPackConc" >> "ProPackSol.csv"
done