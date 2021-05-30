#!/usr/bin/env python3

import pandas as pd
import numpy as np

df = pd.read_csv("nginx_logs",
              sep=" ",
              usecols=[7],
              names=['size'],
              na_values='-',
              header=None
                )

with open('respy.txt', 'w') as f:
  for index, row in df.iterrows():
        f.write("%s\n" % row['size'])


print("Total: ", df['size'].sum())
