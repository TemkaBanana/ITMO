#!/usr/bin/env python3


with open("nginx_logs") as logs:
    with open('respytrue.txt', 'w') as f:
        total = 0
        for line in logs:
            bytes_sent = line.rsplit()[9]
            if bytes_sent != '"-"':
                total += int(bytes_sent)
                f.write("%s\n" % bytes_sent)

print("Total: ", total)
