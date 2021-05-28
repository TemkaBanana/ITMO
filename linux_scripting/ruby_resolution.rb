#!/usr/bin/ruby

def parse_log(log_line)
  p = /^([^ ]*) - ([^ ]*) \[(.*)\] \"(.*)\" (-|[0-9]*) ([0-9]*) \"(.+?|-)\" \"(.+?|-)\"$/.match(log_line)
  return p[6]
end

total = 0

File.foreach("nginx_logs") { |line| total += Integer(parse_log line) }

puts total