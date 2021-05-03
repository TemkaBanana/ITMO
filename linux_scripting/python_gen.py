#!/usr/bin/env python3

with open("nginx_logs") as logs:
    bytecolumn = (line.rsplit()[9] for line in logs)
    bytes_sent = (int(x) for x in bytecolumn if x != '"-"')
    print("Total: ", sum(bytes_sent))
