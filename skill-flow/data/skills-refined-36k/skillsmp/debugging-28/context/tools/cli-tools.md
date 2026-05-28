# Command-Line Debugging Tools

## Log Analysis

### tail - Follow log files
```bash
# Follow log in real-time
tail -f /var/log/app.log

# Last 100 lines
tail -n 100 /var/log/app.log

# Follow multiple files
tail -f /var/log/*.log

# With line numbers
tail -n 100 /var/log/app.log | nl
```

### grep - Search logs
```bash
# Find errors
grep -i "error" app.log

# With context (3 lines before/after)
grep -B3 -A3 "error" app.log

# Count occurrences
grep -c "error" app.log

# Recursive in directory
grep -r "pattern" /var/log/

# Exclude patterns
grep -v "DEBUG" app.log | grep "error"

# Extended regex
grep -E "error|warning|critical" app.log
```

### awk - Log parsing
```bash
# Extract specific column (space-delimited)
awk '{print $1, $5}' access.log

# Filter by condition
awk '$9 >= 500' access.log  # HTTP 500+ errors

# Sum values
awk '{sum += $10} END {print sum}' access.log

# Count by field
awk '{count[$9]++} END {for (c in count) print c, count[c]}' access.log
```

### jq - JSON log parsing
```bash
# Pretty print
cat log.json | jq .

# Extract field
cat log.json | jq '.level'

# Filter
cat log.json | jq 'select(.level == "error")'

# Multiple fields
cat log.json | jq '{time: .timestamp, msg: .message}'
```

## Process Debugging

### ps - Process status
```bash
# All processes with details
ps aux

# Find specific process
ps aux | grep "node"

# Process tree
ps auxf

# By memory usage
ps aux --sort=-%mem | head

# By CPU usage
ps aux --sort=-%cpu | head
```

### top/htop - Live process monitoring
```bash
# Basic top
top

# Better alternative
htop

# In top:
# P - sort by CPU
# M - sort by memory
# k - kill process
# q - quit
```

### lsof - List open files
```bash
# Files opened by process
lsof -p <pid>

# What's using a port
lsof -i :8080

# What's using a file
lsof /var/log/app.log

# Network connections by process
lsof -i -P -n | grep LISTEN
```

### strace - System call tracing
```bash
# Trace process
strace -p <pid>

# Trace new process
strace ./myapp

# Only file operations
strace -e trace=file ./myapp

# Only network operations
strace -e trace=network ./myapp

# With timestamps
strace -t ./myapp

# Save to file
strace -o trace.log ./myapp
```

## Network Debugging

### curl - HTTP requests
```bash
# Basic GET
curl http://localhost:8080/api

# Verbose (see headers)
curl -v http://localhost:8080/api

# POST with JSON
curl -X POST http://localhost:8080/api \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'

# With authentication
curl -H "Authorization: Bearer $TOKEN" http://localhost:8080/api

# Show only headers
curl -I http://localhost:8080/api

# Follow redirects
curl -L http://example.com

# Save response
curl -o response.json http://localhost:8080/api

# Timing breakdown
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8080
```

### netstat/ss - Network connections
```bash
# Listening ports
netstat -tlnp
ss -tlnp

# All connections
netstat -an
ss -an

# Connection statistics
netstat -s
ss -s
```

### nc (netcat) - Network utility
```bash
# Test port connectivity
nc -zv hostname 80

# Simple server
nc -l 8080

# Simple client
echo "hello" | nc hostname 8080

# Port scan
nc -zv hostname 1-1000
```

### tcpdump - Packet capture
```bash
# Capture on interface
tcpdump -i eth0

# Specific port
tcpdump -i eth0 port 80

# Specific host
tcpdump -i eth0 host 192.168.1.1

# Save to file
tcpdump -i eth0 -w capture.pcap

# Read from file
tcpdump -r capture.pcap

# Show packet contents
tcpdump -i eth0 -A port 80
```

### dig/nslookup - DNS lookup
```bash
# Basic lookup
dig example.com
nslookup example.com

# Specific record type
dig example.com MX
dig example.com TXT

# Using specific DNS server
dig @8.8.8.8 example.com

# Trace resolution
dig +trace example.com
```

## Memory Debugging

### free - Memory usage
```bash
# Human readable
free -h

# Continuous monitoring
free -h -s 5  # Every 5 seconds
```

### vmstat - Virtual memory stats
```bash
# Continuous monitoring
vmstat 1  # Every 1 second

# Key columns:
# r - processes waiting to run
# b - processes blocked
# swpd - virtual memory used
# free - idle memory
# si/so - swap in/out
```

### valgrind - Memory error detection (C/C++)
```bash
# Memory errors
valgrind ./myapp

# Memory leaks
valgrind --leak-check=full ./myapp

# Detailed leak info
valgrind --leak-check=full --show-leak-kinds=all ./myapp
```

## Disk Debugging

### df - Disk space
```bash
# Human readable
df -h

# Inodes
df -i

# Specific filesystem
df -h /dev/sda1
```

### du - Directory size
```bash
# Directory sizes
du -sh *

# Largest directories
du -h --max-depth=1 | sort -hr | head

# Specific directory
du -sh /var/log
```

### iostat - Disk I/O
```bash
# Basic stats
iostat

# Continuous monitoring
iostat -x 1  # Extended stats every 1 second

# Key columns:
# %util - device utilization
# await - average wait time
# r/s, w/s - reads/writes per second
```

## Application Debugging

### gdb - GNU Debugger (C/C++)
```bash
# Start with program
gdb ./myapp

# Attach to running process
gdb -p <pid>

# Common commands:
# run - start program
# break main - set breakpoint
# next - next line
# step - step into
# print var - print variable
# backtrace - show stack
# continue - resume
# quit - exit
```

### pdb - Python Debugger
```python
# In code
import pdb; pdb.set_trace()

# From command line
python -m pdb script.py

# Commands:
# n - next line
# s - step into
# c - continue
# p var - print variable
# l - list code
# q - quit
```

### node --inspect - Node.js Debugger
```bash
# Start with inspector
node --inspect app.js

# Break on first line
node --inspect-brk app.js

# Then open chrome://inspect in Chrome
```

## Performance Profiling

### time - Command timing
```bash
# Time a command
time ./myapp

# Outputs:
# real - wall clock time
# user - CPU time in user mode
# sys - CPU time in kernel mode
```

### perf - Linux profiler
```bash
# CPU profiling
perf record ./myapp
perf report

# System-wide
perf top

# Specific events
perf record -e cache-misses ./myapp
```

### py-spy - Python profiler
```bash
# Profile running process
py-spy top --pid <pid>

# Record flame graph
py-spy record -o profile.svg --pid <pid>

# Profile a command
py-spy record -o profile.svg -- python script.py
```

## Quick Reference

| Task | Command |
|------|---------|
| Find process | `ps aux \| grep name` |
| Kill process | `kill -9 <pid>` |
| Port usage | `lsof -i :port` |
| Disk space | `df -h` |
| Memory usage | `free -h` |
| Follow log | `tail -f file.log` |
| Search log | `grep "pattern" file.log` |
| HTTP request | `curl -v url` |
| DNS lookup | `dig hostname` |
| Test port | `nc -zv host port` |
