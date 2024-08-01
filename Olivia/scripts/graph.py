#!/usr/bin/env python3
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import re
import os
import sys

if len(sys.argv) != 3:
    print('provide type, csv file as arguments')
    sys.exit(1)

# method to reformat dataframe (name, types)
def format(df, type):
    for col in df.columns:
        if col == 'Name':
            df['Name'] = df['Name'].replace(r".*_", '', regex=True).replace(r"\.cfg\.txt", '', regex=True) # strip string
            try:
                df['Name'] = df['Name'].astype(float) # convert to float if numeric
            except:
                continue
        else:
            df[col].astype(float) # convert other columns to float

    return df.sort_values(by='Name', ignore_index=True) # sort df rows by 'Name' column

# take in type as an argument
type = sys.argv[1] # 'mixed_cache', 'spec_cache', '3D'

# take in csv file as an argument, load to dataframe
csv = sys.argv[2]
df = format(pd.read_csv(csv), type)
cols = df.columns

slant = False
if len(df.index) > 3: # FIXME: adjust this condition?
    slant = True
if type == 'spec_cache': # 20 / 14 values to plot (comm-dram/sram)
    tot_r = 4
    tot_c = 5
elif type == '3D': # 25 values to plot
    tot_r = 5
    tot_c = 5
elif type == 'mixed_cache': # 11 values to plot
    tot_r = 3
    tot_c = 4

fig, axs = plt.subplots(tot_r, tot_c, figsize=(tot_c * 3, tot_r * 2))
fig.suptitle(csv.replace('_', ' ').replace('.csv', ''))

#FIXME: adjust to stop after columns end
c_i = 1
for r in range(0, tot_r):
    for c in range(0, tot_c):
        axs[r][c].scatter('Name', cols[c_i], data=df)
        axs[r][c].set_title(cols[c_i])
        if slant:
            axs[r][c].tick_params(axis='x', labelrotation=-45)
        # axs[r][c].set_yticks([]) - erase y ticks
        # axs[r][c].set_title(re.sub(r"\(.*\)", "", cols[c_i])) - filter units out of title
        c_i += 1

fig.tight_layout()
plt.show()
