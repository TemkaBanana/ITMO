#!/bin/bash

echo -n "Total:  "
awk '{s+=$10} END {print s}' nginx_logs 
