#!/usr/bin/env python3

import pandas as pd

df = pd.read_csv("nginx_logs",
              sep=' ',
              usecols=[7],
              names=['size'],
              na_values='-',
              header=None
                )

print("Total: ", df['size'].sum())
