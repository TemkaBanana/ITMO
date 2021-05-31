file = File.open("nginx_logs", "r")
lines = file.readlines
total = 0

for line in lines
	bytes_sent = line.split(" ")[9]
	total = total + bytes_sent.to_i
end
puts "Total: #{total}"
file.close