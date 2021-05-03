#!/bin/bash

echo -n "Total:  "
cut -d" " -f 10 nginx_logs | grep ^[0-9]*$ | paste -s -d+ - | bc
