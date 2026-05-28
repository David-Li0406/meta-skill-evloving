# Hash IOC Examples

## Basic Hash File

Filename: `incident-hashes.txt`

```text
# Operation Sunrise - Malware Hashes
# Collected from incident response engagement

# Dropper component (SHA256)
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855;Dropper stage 1

# Main payload (MD5)
d41d8cd98f00b204e9800998ecf8427e;Main RAT payload

# Lateral movement tool (SHA1)
da39a3ee5e6b4b0d3255bfef95601890afd80709;PSExec variant
```

## Hash File with Custom Scores

Filename: `tiered-hashes.txt`

```text
# Critical - Confirmed malware
aabbccdd11223344556677889900aabb;100;Confirmed APT backdoor

# High - Likely malicious
11223344556677889900aabbccddeeff;80;Suspicious packer

# Medium - Needs investigation
ffeeddccbbaa99887766554433221100;50;Potentially unwanted tool

# Low - Anomaly detection
00112233445566778899aabbccddeeff;30;Unusual but possibly legitimate
```

## Imphash Detection

Filename: `imphash-iocs.txt`

```text
# Cobalt Strike Beacon imphashes
# Reference: https://github.com/Neo23x0/signature-base

d0583e7f5e56a9621b4fe9e4d65ab347;Cobalt Strike default imphash
36b3e0e57f3e59e4eaaddc8e2bae1b1a;Cobalt Strike reflective loader

# Mimikatz variants
3a5aca6e9c03b3e3e3a6e3e3e3a5aca6;Mimikatz x64
```

## Trusted Hash Whitelist

Filename: `our-trusted-hashes.txt`

```text
# Internal tools - reduce false positives

# Our custom admin scripts
abc123def456789...;Internal deployment script
def456abc789012...;Monitoring agent installer

# Vendor tools we use
789abc123def456...;Approved remote support tool
```

## Mixed Hash Types

Filename: `campaign-x-hashes.txt`

```text
# Campaign X IOCs - Mixed hash types
# Source: Threat Intel Team

# MD5 (32 chars)
d41d8cd98f00b204e9800998ecf8427e;Stage 1 loader

# SHA1 (40 chars)
da39a3ee5e6b4b0d3255bfef95601890afd80709;Stage 2 payload

# SHA256 (64 chars)
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855;Final payload

# Imphash (32 chars, must specify it's imphash in comment for clarity)
d0583e7f5e56a9621b4fe9e4d65ab347;Imphash - packed variant
```

## Usage

```bash
# Copy to THOR custom-signatures folder
cp incident-hashes.txt /path/to/thor/custom-signatures/

# Run scan
./thor-macosx -p /target

# Run with only custom signatures
./thor-macosx --customonly -p /target
```
