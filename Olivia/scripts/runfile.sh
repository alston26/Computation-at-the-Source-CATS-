#!/usr/bin/env bash
config=$1
cd cacti || exit
./cacti -infile "../$config" > "${config#*/}".txt || exit
mv ./*.txt ..
echo "ran $config"