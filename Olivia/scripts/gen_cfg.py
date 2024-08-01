#!/usr/bin/env python3
import sys
import shutil

config = sys.argv[1]
to_write = sys.argv[2]

shutil.copy('cacti_sweeps/sweep.cfg', config)

f = open(config, 'a')
f.write(to_write) 
f.close()