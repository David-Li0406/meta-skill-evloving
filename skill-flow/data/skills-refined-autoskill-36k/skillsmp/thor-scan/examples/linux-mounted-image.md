# Linux Mounted Image Examples

## Mounted Windows Image

```bash
./thor-linux-64 --lab \
  -p /mnt/image \
  --virtual-map /mnt/image:C \
  -j YOURHOST \
  -e /cases/case001/reports
```

- `--lab`: Enables intense mode, multi-threading, cross-platform IOCs
- `--virtual-map /mnt/image:C`: Maps mount point to original C: drive
- `-j YOURHOST`: Preserves original hostname in logs
- `-e`: Output directory

## Mounted Linux Image

```bash
./thor-linux-64 --lab \
  -p /mnt/image \
  --virtual-map /mnt/image:/ \
  -j YOURHOST \
  -e /cases/case001/reports
```

## Multiple Partitions

```bash
# Scan each partition separately
./thor-linux-64 --lab -p /mnt/part1 --virtual-map /mnt/part1:C -j HOST -e /out
./thor-linux-64 --lab -p /mnt/part2 --virtual-map /mnt/part2:D -j HOST -e /out
```

## With Audit Trail (v11)

```bash
./thor-linux-64 --lab \
  -p /mnt/image \
  --virtual-map /mnt/image:C \
  -j YOURHOST \
  --audit-trail /cases/case001/YOURHOST_audit.json.gz \
  -e /cases/case001/reports
```

## With JSON Output

```bash
./thor-linux-64 --lab \
  -p /mnt/image \
  --virtual-map /mnt/image:C \
  -j YOURHOST \
  --jsonfile /cases/case001/YOURHOST.json \
  -e /cases/case001/reports
```

## Limit Threads (Multiple Parallel Scans)

```bash
# On a 16-core system running 4 parallel image scans
./thor-linux-64 --lab --threads 4 \
  -p /mnt/image1 \
  --virtual-map /mnt/image1:C \
  -j HOST1 \
  -e /cases/case001/reports
```

## Without Lab License (Limited)

```bash
./thor-linux-64 -a Filescan --intense -p /mnt/image
```

Missing: virtual mapping, hostname override, cross-platform IOCs, multi-threading.

## Scan Specific Subdirectory

```bash
./thor-linux-64 --lab \
  -p /mnt/image/Users/Administrator \
  --virtual-map /mnt/image:C \
  -j YOURHOST \
  -e /reports
```

## With Signature Filtering

```bash
./thor-linux-64 --lab \
  --init-selector RANSOM,Lockbit \
  -p /mnt/image \
  --virtual-map /mnt/image:C \
  -j YOURHOST \
  -e /reports
```
