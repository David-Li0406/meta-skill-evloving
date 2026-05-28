# Linux Debug Cookbook

## System-Level Debugging

### Process Analysis Deep Dive

```bash
# Real-time process monitoring with resource tracking
strace -f -e trace=open,stat,read,write -p PID 2>&1 | tee debug.log

# Memory maps and allocation analysis
pmap -x PID | sort -k3 -n
cat /proc/PID/maps
cat /proc/PID/smaps  # Detailed memory info

# Find what's keeping files open
lsof -p PID | grep -E 'REG|DIR'
ls -la /proc/PID/fd

# Network connections and sockets
ss -anp | grep PID
netstat -tulpn | grep PID

# CPU affinity and scheduling
taskset -cp PID
chrt -p PID

# I/O statistics
iotop -p PID
iostat -x 1
```

### Kernel and System Tracing

```bash
# eBPF-based tracing (requires bpftrace)
bpftrace -e 'tracepoint:syscalls:sys_enter_* { @[probe] = count(); }'

# Kernel trace events
echo 1 > /sys/kernel/debug/tracing/events/sched/enable
cat /sys/kernel/debug/tracing/trace_pipe

# Performance profiling
perf record -F 99 -p PID -g -- sleep 10
perf report --stdio

# System-wide syscall analysis
sysdig -w capture.scap
sysdig -r capture.scap proc.name=myapp

# ftrace function tracing
echo function > /sys/kernel/debug/tracing/current_tracer
echo 1 > /sys/kernel/debug/tracing/tracing_on
```

### Network Debugging Arsenal

```bash
# Deep packet inspection
tcpdump -i any -w capture.pcap -v host IPADDR
tshark -r capture.pcap -Y "tcp.port == 443"

# SSL/TLS debugging
openssl s_client -connect host:443 -showcerts -debug
ssldump -i eth0 port 443

# DNS troubleshooting
drill @8.8.8.8 domain.com
dig +trace domain.com
nslookup -debug domain.com

# Connection tracking
conntrack -L | grep ESTABLISHED
netstat -anp | awk '$6 == "ESTABLISHED"'

# MTU and path discovery
tracepath -n host
ip route get host

# Bandwidth testing
iperf3 -s  # Server
iperf3 -c SERVER_IP -t 30 -i 1  # Client
```

## Nix-Specific Debugging

### Build Debugging

```bash
# Enable verbose Nix builds
nix build --show-trace --print-build-logs --verbose .#package

# Debug failing build
nix develop .#package --command bash
cd /build/source
# Manually run build steps

# Inspect build environment
nix-shell '<nixpkgs>' -A package
printenv | grep -E 'NIX|PATH|PREFIX'

# Check derivation details
nix derivation show .#package
nix show-derivation /nix/store/...-package.drv

# Trace evaluation
nix eval --show-trace .#package.meta

# Profile evaluation performance
nix eval --profile=profile.json .#nixosConfigurations.hostname.config.system.build.toplevel
```

### Dependency Analysis

```bash
# Why is this package in closure?
nix-store --query --tree /run/current-system
nix why-depends /run/current-system /nix/store/...-package

# Closure size analysis
nix path-info -Sh .#package
nix path-info -rsh .#package | sort -hk2 | tail -20

# Find reverse dependencies
nix-store --query --referrers /nix/store/...-package

# Garbage collection dry-run
nix-store --gc --print-dead | head -20
nix-store --gc --print-live | grep package
```

### Runtime Debugging

```bash
# Enable Nix debug mode
NIX_DEBUG=1 nix-shell

# Check what's in PATH
nix eval .#devShells.x86_64-linux.default.buildInputs --json | jq

# Trace Nix operations
nix --option trace-function-calls true build .#package 2>&1 | tee trace.log

# Remote build debugging
nix build --builders 'ssh://builder@remote' --log-format raw
```

## Storage and Filesystem Debugging

```bash
# Disk I/O analysis
iotop -aoP
blktrace -d /dev/sda -o trace
blkparse trace.blktrace.0

# Filesystem performance
df -i  # Inode usage
du -sh /* | sort -h
find / -xdev -type f -size +100M

# Detect filesystem errors
dmesg | grep -i error
journalctl -k | grep -i 'filesystem\|i/o'

# SMART monitoring
smartctl -a /dev/sda
smartctl -H /dev/sda

# Mount debugging
mount | column -t
cat /proc/mounts
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE

# Check for deleted files still open
lsof +L1

# Find files by access time
find /var -type f -atime -1  # Accessed in last 24h
```

## Memory Debugging

```bash
# Memory leak detection
valgrind --leak-check=full --show-leak-kinds=all ./program

# Monitor memory usage patterns
ps aux --sort=-%mem | head -10
smem -t -k -p | head -20

# Analyze core dumps
coredumpctl list
coredumpctl debug PID
gdb program core.PID

# Check for OOM killer activity
journalctl -xe | grep -i 'oom\|killed'
dmesg -T | grep -i oom

# Memory pressure monitoring
cat /proc/pressure/memory
systemd-cgtop
```

## Container and Namespace Debugging

```bash
# Enter namespace of running process
nsenter -t PID -n -u -i -m -p bash

# Inspect container namespaces
lsns -p PID
ls -la /proc/PID/ns/

# cgroup analysis
systemd-cgls
cat /proc/PID/cgroup

# Container network debugging
docker inspect CONTAINER | jq '.[0].NetworkSettings'
ip netns list
ip netns exec NAMESPACE ip addr

# Troubleshoot container storage
docker system df
docker system df -v
```

## Binary Analysis and Reverse Engineering

```bash
# Executable analysis
file /path/to/binary
ldd /path/to/binary
readelf -a /path/to/binary | less

# Symbol table inspection
nm -C /path/to/binary | grep function
objdump -t /path/to/binary

# Dynamic analysis
ltrace -c ./program
ltrace -f -e '@libc.so*' ./program

# Disassembly
objdump -d -M intel /path/to/binary | less
radare2 -A /path/to/binary

# Strings extraction
strings -n 8 /path/to/binary | grep -i password

# Check security features
checksec --file=/path/to/binary
readelf -l binary | grep GNU_STACK
```

## Service and Systemd Debugging

```bash
# Analyze service failures
systemctl status service-name --full --no-pager
journalctl -xeu service-name -n 100 --no-pager

# Service dependency analysis
systemd-analyze plot > boot.svg
systemd-analyze critical-chain service-name

# Check socket activation
systemctl list-sockets --all
ss -lnp | grep systemd

# Trace service execution
systemd-run --scope -p 'ExecStartPre=strace -f -o /tmp/trace.log' service

# Test service in isolation
systemd-run --user --scope bash
# Then manually start the service

# Resource limits debugging
systemctl show service-name | grep -i limit
cat /sys/fs/cgroup/system.slice/service-name/memory.max
```

## Advanced Troubleshooting Patterns

### Race Condition Detection

```bash
# Repeat test until failure
while ./test.sh; do echo "Pass"; done

# Parallel stress test
for i in {1..100}; do ./program & done
wait

# Time-sensitive debugging
time strace -tt -T ./program
```

### Permission and Security Issues

```bash
# Audit file access attempts
auditctl -w /path/to/file -p war -k filewatch
ausearch -k filewatch

# AppArmor troubleshooting
aa-status
aa-logprof
journalctl | grep apparmor

# SELinux debugging
ausearch -m avc -ts recent
audit2why < /var/log/audit/audit.log
```

### Environmental Reproduction

```bash
# Capture full environment
env > env-before.txt
# Run failing operation
env > env-after.txt
diff env-before.txt env-after.txt

# Isolate environment variables
env -i PATH=/usr/bin HOME=/tmp ./program

# Library loading debug
LD_DEBUG=libs ./program 2>&1 | tee ld-debug.log
LD_PRELOAD=/path/to/lib.so ./program
```
