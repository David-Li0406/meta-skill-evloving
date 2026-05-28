# Memory Dump Scan Examples

## Direct Memory Image Scan (DeepDive)

```bash
./thor-linux-64 --lab \
  --image_file /path/to/memory.dmp \
  -j YOURHOST \
  -e /cases/reports
```

DeepDive processes overlapping 3MB chunks and reports byte offsets.

## Memory Image with PE File Restoration

```bash
./thor-linux-64 --lab \
  --image_file /path/to/memory.dmp \
  -r /cases/restored_files/ \
  -j YOURHOST \
  -e /cases/reports
```

Restores PE files matching YARA rules to `-r` directory for further analysis.

## Memory Image with Audit Trail (v11)

```bash
./thor-linux-64 --lab \
  --image_file /path/to/memory.dmp \
  --audit-trail /cases/YOURHOST_audit.json.gz \
  -j YOURHOST \
  -e /cases/reports
```

## Scan Extracted Process Dumps (Volatility)

First, extract process memory with Volatility:
```bash
vol.py -f memory.raw --profile=Win10x64_19041 memdump -D /cases/procs/
```

Then scan the extracted dumps:
```bash
./thor-linux-64 --lab \
  -p /cases/procs/ \
  -j YOURHOST \
  -e /cases/reports
```

## Scan Volatility-Extracted DLLs

Extract DLLs:
```bash
vol.py -f memory.raw --profile=Win10x64_19041 dlldump -D /cases/dlls/
```

Scan:
```bash
./thor-linux-64 --lab \
  -p /cases/dlls/ \
  -j YOURHOST \
  -e /cases/reports
```

## Scan AVML Linux Memory Dump

```bash
./thor-linux-64 --lab \
  --image_file /path/to/avml_dump.lime \
  -j LINUXHOST \
  -e /cases/reports
```

## Windows: Memory Image Scan

```bash
thor64.exe --lab ^
  --image_file C:\cases\memory.dmp ^
  -j YOURHOST ^
  -e C:\cases\reports
```

## Targeted Hunt in Memory

```bash
./thor-linux-64 --lab \
  --image_file /path/to/memory.dmp \
  --init-selector Cobalt,Beacon \
  -j YOURHOST \
  -e /cases/reports
```

## Hibernation File Scan

Scan Windows hibernation file (hiberfil.sys) from mounted image:
```bash
./thor-linux-64 --lab \
  --image_file /mnt/image/hiberfil.sys \
  -j YOURHOST \
  -e /cases/reports
```

## Notes

- Memory scans are intensive; expect longer runtimes
- `--image_file` uses DeepDive: overlapping chunks, byte-offset reporting
- PE restoration (`-r`) creates files that can be submitted to VirusTotal or sandboxes
- Extracted dumps from Volatility scan faster than raw memory images
- DeepDive chunk size equals `max_file_size` setting
