# Case from Mounted Image

Workflow for analyzing a forensic disk image with THOR Lens.

## Prerequisites

- THOR v11 installed and licensed
- THOR Lens built (`make build`)
- Forensic disk image mounted

## Step 1: Mount the Image

### Using ewfmount (E01 images)

```bash
sudo mkdir -p /mnt/ewf /mnt/image
sudo ewfmount /path/to/image.E01 /mnt/ewf
sudo mount -o ro,loop /mnt/ewf/ewf1 /mnt/image
```

### Using mount (raw images)

```bash
sudo mkdir -p /mnt/image
sudo mount -o ro,loop /path/to/image.dd /mnt/image
```

### Verify Mount

```bash
ls /mnt/image/
# Should show Windows or Linux filesystem contents
```

## Step 2: Identify Original Hostname

For Windows images:

```bash
cat /mnt/image/Windows/System32/config/SYSTEM 2>/dev/null | strings | grep -i "ComputerName"
# or
cat /mnt/image/Windows/System32/drivers/etc/hosts | head
```

For Linux images:

```bash
cat /mnt/image/etc/hostname
```

Use this hostname with `-j` flag.

## Step 3: Run THOR v11 Scan

### Windows Image Mounted on Linux

```bash
./thor-linux-64 --lab \
  -p /mnt/image \
  --virtual-map /mnt/image:C \
  -j WORKSTATION01 \
  --audit-trail /cases/WORKSTATION01_audit.jsonl \
  -e /cases/reports
```

**Critical flags:**
- `--virtual-map /mnt/image:C` - Maps paths correctly in events
- `-j WORKSTATION01` - Sets correct hostname in events

### Linux Image

```bash
./thor-linux-64 --lab \
  -p /mnt/image \
  --virtual-map /mnt/image:/ \
  -j linuxserver01 \
  --audit-trail /cases/linuxserver01_audit.jsonl \
  -e /cases/reports
```

### Multiple Partitions

If image has multiple partitions:

```bash
# Mount each partition
sudo mount -o ro,loop,offset=... /path/to/image.dd /mnt/part1
sudo mount -o ro,loop,offset=... /path/to/image.dd /mnt/part2

# Scan each with appropriate virtual map
./thor-linux-64 --lab -p /mnt/part1 --virtual-map /mnt/part1:C -j HOST --audit-trail /cases/HOST_C.jsonl
./thor-linux-64 --lab -p /mnt/part2 --virtual-map /mnt/part2:D -j HOST --audit-trail /cases/HOST_D.jsonl
```

## Step 4: Verify Audit Trail

```bash
# Check file size
ls -lh /cases/WORKSTATION01_audit.jsonl

# Preview content
head -3 /cases/WORKSTATION01_audit.jsonl | jq .

# Check paths look correct (should show C:\... not /mnt/image/...)
zcat /cases/WORKSTATION01_audit.jsonl | head -100 | jq '.object.path' | head
```

## Step 5: Import into THOR Lens

```bash
cd /path/to/thor-lens

./thorlens import \
  --log /cases/WORKSTATION01_audit.jsonl \
  --case WORKSTATION01

# Verify
cat ./cases/WORKSTATION01/meta.json | jq '.event_count'
```

## Step 6: Start Server and Analyze

```bash
./thorlens serve --case ./cases/WORKSTATION01 --port 8080
```

Open **http://127.0.0.1:8080**

### Analysis Tips for Forensic Images

1. **Start with high-score events** - Switch histogram to "score" mode
2. **Check temporal clusters** - Unusual activity spikes often indicate compromise
3. **Follow paths** - Use path filter to explore suspicious directories
4. **Correlate timestamps** - Look for activity chains around known events
5. **Tag as you go** - Mark suspicious items for later review

## Step 7: Cleanup

```bash
# Unmount image
sudo umount /mnt/image
sudo umount /mnt/ewf  # if using ewfmount

# Remove mount points
sudo rmdir /mnt/image /mnt/ewf
```

## Common Issues

### Paths Show /mnt/image Instead of C:\

Missing `--virtual-map` flag. Re-run scan:

```bash
./thor-linux-64 --lab -p /mnt/image --virtual-map /mnt/image:C -j HOST --audit-trail output.jsonl
```

### Hostname Shows Analysis Workstation

Missing `-j` flag. Re-run scan:

```bash
./thor-linux-64 --lab -p /mnt/image -j ORIGINAL_HOSTNAME --audit-trail output.jsonl
```

### Permission Denied Errors

Run as root:

```bash
sudo ./thor-linux-64 --lab ...
```

## Quick Reference

```bash
# Full command for Windows image
./thor-linux-64 --lab \
  -p /mnt/image \
  --virtual-map /mnt/image:C \
  -j HOSTNAME \
  --audit-trail /cases/HOSTNAME_audit.jsonl \
  -e /cases/reports

# Import
./thorlens import --log /cases/HOSTNAME_audit.jsonl --case HOSTNAME

# Serve
./thorlens serve --case ./cases/HOSTNAME --port 8080
```
