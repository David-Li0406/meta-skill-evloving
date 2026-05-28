# Enhanced YARA Rule Examples

## Basic Rule with Score

```yara
rule Malware_Indicator_1 {
    meta:
        description = "Detects malware family X"
        author = "Your Name"
        score = 80
    strings:
        $s1 = "malicious_export" ascii
        $s2 = { 4D 5A 90 00 03 00 00 00 }
    condition:
        all of them
}
```

## Using External Variables

### Filename and Extension

```yara
rule Suspicious_DLL_Location {
    meta:
        description = "DLL in user temp folder"
        score = 60
    condition:
        extension == ".dll" and
        filepath matches /\\Users\\[^\\]+\\AppData\\Local\\Temp/
}
```

### Filetype Detection

```yara
rule EXE_Masquerading_As_Doc {
    meta:
        description = "Executable with document extension"
        score = 90
    condition:
        filetype == "EXE" and
        extension matches /\.(doc|pdf|txt|xlsx)$/i
}
```

### Unpack Source

```yara
rule Suspicious_EXE_In_Email_Attachment {
    meta:
        description = "EXE extracted from email"
        score = 70
    condition:
        filetype == "EXE" and
        unpack_source contains "EMAIL"
}

rule Double_Packed {
    meta:
        description = "File with multiple archive layers"
        score = 50
    condition:
        unpack_source matches /ZIP.*ZIP/ or
        unpack_source matches /RAR.*RAR/
}
```

## Memory-Only Rules

```yara
rule Cobalt_Strike_Beacon_Memory {
    meta:
        description = "Cobalt Strike beacon in memory"
        type = "memory"
        score = 100
    strings:
        $s1 = "%s as %s\\%s: %d" ascii
        $s2 = "beacon.dll" ascii
        $s3 = "%s (admin)" ascii
    condition:
        2 of them
}
```

## File-Only Rules

```yara
rule Suspicious_PDB_Path {
    meta:
        description = "Suspicious PDB path in executable"
        type = "file"
        score = 70
    strings:
        $pdb1 = /C:\\Users\\[a-z]+\\.*\.pdb/ ascii
        $pdb2 = "\\Release\\payload.pdb" ascii
    condition:
        any of them and filetype == "EXE"
}
```

## Module-Limited Rules

```yara
rule Suspicious_Mutex {
    meta:
        description = "Known malicious mutex"
        limit = "Mutex"
        score = 90
    strings:
        $m1 = "Global\\EVIL_MUTEX_123"
        $m2 = "BaseNamedObjects\\apt_mutex"
    condition:
        any of them
}
```

## Registry Rules

File: `persistence-registry.yar`

```yara
rule Registry_RunKey_Suspicious {
    meta:
        description = "Suspicious Run key entry"
        score = 70
    strings:
        $run = "\\CurrentVersion\\Run;" nocase
        $susp1 = ";powershell" nocase
        $susp2 = ";cmd.exe /c" nocase
        $susp3 = ";mshta" nocase
    condition:
        $run and any of ($susp*)
}

rule Registry_Service_ImagePath {
    meta:
        description = "Service with suspicious image path"
        score = 60
    strings:
        $svc = "\\Services\\" nocase
        $img = ";ImagePath;" nocase
        $susp = /;ImagePath;[^;]*\\Users\\/ nocase
    condition:
        $svc and $img and $susp
}
```

## Log Rules

File: `suspicious-log.yar`

```yara
rule EventLog_PowerShell_Download {
    meta:
        description = "PowerShell download command in logs"
        score = 75
    strings:
        $ps = "powershell" nocase
        $dl1 = "downloadstring" nocase
        $dl2 = "downloadfile" nocase
        $dl3 = "wget" nocase
        $dl4 = "curl" nocase
    condition:
        $ps and any of ($dl*)
}
```

## Meta Rules with DEEPSCAN Trigger

```yara
rule Trigger_DeepScan_Large_Archive : DEEPSCAN {
    meta:
        description = "Force deep scan on large archives"
        score = 0
    condition:
        (filetype == "ZIP" or filetype == "RAR") and
        filesize > 50MB
}

rule Trigger_DeepScan_Suspicious_Name : DEEPSCAN {
    meta:
        description = "Deep scan files with suspicious names"
        score = 0
    condition:
        filename matches /^(update|install|setup)\d+\.exe$/i
}
```

## False Positive Rules

```yara
rule FP_McAfee_Signatures {
    meta:
        description = "McAfee signature file"
        falsepositive = 1
        score = 50
    strings:
        $s1 = "McAfee" ascii
        $s2 = "DAT file" ascii
    condition:
        all of them and extension == ".dat"
}

rule FP_AV_Quarantine {
    meta:
        description = "AV quarantine folder"
        falsepositive = 1
        score = 40
    condition:
        filepath matches /\\Quarantine\\/ or
        filepath matches /\\Vault\\/
}
```

## Combined Conditions

```yara
rule APT_Backdoor_Combo {
    meta:
        description = "APT backdoor indicators"
        author = "Threat Intel Team"
        score = 95
    strings:
        $s1 = "beacon" ascii fullword
        $s2 = "PAYLOAD_KEY" ascii
        $pdb = "\\Release\\implant.pdb" ascii
    condition:
        filetype == "EXE" and
        filesize < 500KB and
        (2 of ($s*) or $pdb) and
        not filepath matches /\\Windows\\/
}
```

## Deployment

```bash
# Place in yara subfolder
cp my-rules.yar /path/to/thor/custom-signatures/yara/

# For registry rules, include 'registry' in filename
cp persistence-registry.yar /path/to/thor/custom-signatures/yara/

# For log rules, include 'log' in filename
cp suspicious-log.yar /path/to/thor/custom-signatures/yara/
```
