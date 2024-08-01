#!/usr/bin/env bash
direc="$1" # take in directory name as argument
mkdir "cacti_sweeps/$direc" || exit # create directory in cacti_sweeps
echo "new directory: cacti_sweeps/$direc"
cd "cacti_sweeps" || exit
mkdir "$direc"/configs && mkdir "$direc"/results && mkdir "$direc"/output # create subdirectories
mv ../*.cfg "$direc"/configs # move runfile.sh output into directories
mv ../*.txt "$direc"/results
mv ../*.out "$direc"/output 
echo 'sorted'
