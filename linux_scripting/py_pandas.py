#!/usr/bin/env python3

import pandas as pd

df = pd.read_csv("nginx_logs",
              sep=r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)(?![^\[]*\])',
              engine='python',
              usecols=[0, 3, 4, 5, 6, 7, 8],
              names=['ip', 'time', 'request', 'status', 'size', 'referer', 'user_agent'],
              na_values='"-"',
              header=None
                )

print("Total: ", df['size'].sum())

