#!/usr/bin/env bash
category=$1 # take in sweep category as argument
cd cacti_sweeps || exit
ls -d -- */ | grep -v '_sweeps' | grep -v 'csv.*' | xargs -I {} mv {} "$category/configs_outputs" # move parameter folders into configs_outputs direc
mv ../*.csv "$category/csv" # move csv files into csv directory
