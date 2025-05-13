#!/bin/bash

for yr in {2006..2019}; do
	echo "Downloading $yr ..."
	sed s/0000/${yr}/g Td_surfaceTPr.py > Td_surfaceTPr_tmp.py
	python Td_surfaceTPr_tmp.py
done
