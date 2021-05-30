
#!/usr/bin/env python3
import math
import pandas as pd

df = pd.read_csv("nginx_logs",
              sep=r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)(?![^\[]*\])',
              engine='python',
              usecols=[6],
              names=['size'],
	      na_values='"-"',
              header=None
                )

s = 0

for d in df['size']:
    if not math.isnan(d):
        s+=int(d)

print("Tot: ", s)
print("Size = ",df['size'].size)
print("Total: ", df['size'].sum())

