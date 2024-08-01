#!/usr/bin/env python3
import subprocess
import sys
import os

"""
Wrapper for gen_config.py, runfile.sh, gen_csv.py, graph.py subprocesses.
"""

parameter = 'dram dimm' # "dram type"
values = ['"UDIMM"', '"RDIMM"', '"LRDIMM"'] # ['DDR3', 'DDR4']
mid = ' ' # " (Gb) "
type = 'spec_cache' # '3D', 'mixed_cache', 'spec_cache'

formatted_parameter = parameter.replace(' ', '_')

for v in values:
    # generate config file
    config = f"{formatted_parameter}_{v}.cfg"
    to_write = f"-{parameter}{mid}{v}"
    subprocess.call(f"scripts/gen_cfg.py '{config}' '{to_write}'", shell=True) # takes config filename and line to write

    if config in os.listdir():
        # adjust to .call if not waiting properly
        subprocess.run(f"scripts/runfile.sh '{config}'", shell=True, executable="/bin/bash")
    else:
        print('config file not found')

# sort output to a directory, generate csv file, produce graph of output
subprocess.call(f"scripts/sort.sh {formatted_parameter}", shell=True, executable="/bin/bash") # takes in directory name
subprocess.call(f"scripts/gen_csv.py {type} {formatted_parameter}", shell=True) # takes type and parameter
subprocess.call(f"scripts/graph.py {type} {formatted_parameter}.csv", shell=True)

print("done")
