#!/usr/bin/asql -f

load nginx_logs_with_header
select sum(size) from logs
