#!/usr/bin/env python3
import shutil
import os
import sys
import re

#FIXME: modify script to work even if input params not printed

if len(sys.argv) != 3:
    print('provide type and parameter as arguments')
    sys.exit(1)

# take type and parameter as arguments, create csv file to write to
type = sys.argv[1] # '3D', 'mixed_cache', 'spec_cache'
directory = f"cacti_sweeps/{sys.argv[2]}/results"
new_csv = f"{sys.argv[2]}.csv"

# iterate through files in given directory
for filename in os.listdir(directory):
    file = os.path.join(directory, filename)
    results = open(file, 'r')
    lines = results.readlines()
    lines = list(map(lambda x: x.rstrip(), lines))

    # find specific model
    spec = ''
    if type in ['mixed_cache', 'spec_cache']:
        model = lines[45][lines[45].index('2), ')+4:lines[45].index('-', 12)-1]
        if model == 'Uniform Cache Access Commodity DRAM Model':
            spec = 'uca_comm-dram'
        elif model == 'Uniform Cache Access SRAM Model':
            spec = 'uca_sram'
        elif model == 'Uniform Cache Access Logic Process Based DRAM Model':
            spec = 'uca_lp-dram'
        else:
            print('specific model not defined')
            sys.exit(1)

    # load csv file depending on type/spec
    if filename == os.listdir(directory)[0]:
        if type == 'spec_cache':
            csv = shutil.copy(f"cacti_sweeps/csv_headings/{spec}_headings.csv", new_csv)
            f = open(new_csv, 'a')
        else:
            csv = shutil.copy(f"cacti_sweeps/csv_headings/{type}_headings.csv", new_csv)
        f = open(new_csv, 'a')

    # write name, IO results to csv regardless of type
    f.write("\n" + filename)
    for i in range(39, 44): # IO results in lines 40-44
        if i == 42:
            eqs = [j.start() for j in re.finditer('=', lines[i])]
            for eq in eqs: 
                f.write(f", {re.sub(r"[a-zA-Z ]", '', lines[i][eq+2:eq+12])}")
        else:
            f.write(f", {lines[i][lines[i].index('=')+2:]}")

    # parse values specific to 3D DRAM
    if type == '3D':
        for i in range(61, 82): # previous numbers : (62, 83)
            if i in [67, 72, 78]: # previously : [68, 73, 79]
                continue
            else:
                f.write(f", {re.sub(r"[a-zA-Z %]", '', lines[i][lines[i].index(':')+2:])}")
    
    # parse values for cache model
    if type in ['mixed_cache', 'spec_cache']:
        
        # final line to read depends on spec
        hi = 63 # 63 for 'uca_sram', 'uca_lp-dram'
        if spec == 'uca_comm-dram':
                hi = 68

        # set lines to parse based on type
        lines_list = list(range(57, hi+1)) # list for 'spec_cache'
        if type == 'mixed_cache':
            lines_list = [57, 58, hi] 

        #FIXME: possible issue- line 58 writes an extra space
        for i in lines_list: 
            if i == hi:
                colon = lines[i].index(':')
                x = lines[i].index('x', colon)
                f.write(f", {lines[i][colon+2:x-1]}")
                f.write(f", {lines[i][x+2:]}")
            else:
                f.write(f", {lines[i][lines[i].index(':')+2:]}")       

f.close()
print("csv generated")