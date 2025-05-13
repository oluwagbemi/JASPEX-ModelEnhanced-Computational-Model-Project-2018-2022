#!/bin/bash

for yr in {2006..2011}; do
	echo "Downloading $yr ..."
	sed s/0000/${yr}/g rhPressLev1000hPa.py > rhPressLev1000hPa_tmp.py
	python rhPressLev1000hPa_tmp.py
done
