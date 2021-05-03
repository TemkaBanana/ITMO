#!/usr/bin/env python3


with open("nginx_logs") as logs:
    total = 0
    for line in logs:
        bytes_sent = line.rsplit()[9]
        if bytes_sent != '"-"':
            total += int(bytes_sent)
    print("Total: ", total)
