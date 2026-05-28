# S3 Artifact Retrieval Guide

Instructions for coworkers to download and examine session-chronicle artifacts from S3.

**ADR**: [Session Chronicle S3 Sharing](/docs/adr/2026-01-02-session-chronicle-s3-sharing.md)

---

## Prerequisites

Install required tools:

```bash
brew install brotli awscli 1password-cli
```

Sign in to 1Password:

```bash
op signin
```

Verify access to Claude Automation vault:

```bash
op read "op://Claude Automation/ise47dxnkftmxopupffavsgby4/access key id" >/dev/null && echo "OK"
```

---

## Retrieval Workflow

```
                        Session Chronicle S3 Retrieval Workflow

 -----------      ###############     +-------------+     +------------+      ----------
| 1Password |     # Export AWS  #     | aws s3 sync |     | brotli -d  |     | Analyze  |
|   Auth    | --> # Credentials # --> |  Download   | --> | Decompress | --> | Sessions |
 -----------      ###############     +-------------+     +------------+      ----------
```

<details>
<summary>graph-easy source</summary>

```
graph { label: "Session Chronicle S3 Retrieval Workflow"; flow: east; }
[ 1Password\nAuth ] { shape: rounded; } -> [ Export AWS\nCredentials ] { border: bold; } -> [ aws s3 sync\nDownload ] -> [ brotli -d\nDecompress ] -> [ Analyze\nSessions ] { shape: rounded; }
```

</details>

---

## Quick Retrieval

### Option 1: Using the retrieval script

```bash
# Clone the cc-skills repo (if needed)
git clone https://github.com/terrylica/cc-skills.git

# Run retrieval script
cd cc-skills/plugins/devops-tools/skills/session-chronicle
./scripts/retrieve_artifact.sh s3://eonlabs-findings/sessions/<id>/ ./artifacts
```

### Option 2: Manual retrieval

Copy this command from the git commit message:

```bash
/usr/bin/env bash << 'RETRIEVE_EOF'
export AWS_ACCESS_KEY_ID=$(op read "op://Claude Automation/ise47dxnkftmxopupffavsgby4/access key id")
export AWS_SECRET_ACCESS_KEY=$(op read "op://Claude Automation/ise47dxnkftmxopupffavsgby4/secret access key")
export AWS_DEFAULT_REGION="us-west-2"
aws s3 sync s3://eonlabs-findings/sessions/<id>/ ./artifacts/
for f in ./artifacts/*.br; do brotli -d "$f"; done
RETRIEVE_EOF
```

---

## Understanding the Artifacts

After retrieval, your `./artifacts/` directory will contain:

| File               | Description                                                             |
| ------------------ | ----------------------------------------------------------------------- |
| `manifest.json`    | Metadata about the session chain (timestamps, line counts, S3 location) |
| `uuid_chain.jsonl` | NDJSON trace of UUID chain from target to origin                        |
| `*.jsonl.br`       | Brotli-compressed session files                                         |
| `*.jsonl`          | Decompressed session files (after running `brotli -d`)                  |

### Examining Session Files

Session files are NDJSON (newline-delimited JSON). Each line is a conversation entry:

```bash
# View first few entries
head -5 ./artifacts/<session-id>.jsonl | jq .

# Search for specific tool uses
jq -c 'select(.message.content[]?.type == "tool_use")' ./artifacts/<session-id>.jsonl

# Find Edit operations
jq -c 'select(.message.content[]?.name == "Edit")' ./artifacts/<session-id>.jsonl
```

### Tracing UUID Chain

The `uuid_chain.jsonl` shows the provenance path:

```bash
# View the chain
cat ./artifacts/uuid_chain.jsonl | jq .

# Get session IDs in chain
jq -r '.session_id' ./artifacts/uuid_chain.jsonl | sort -u
```

---

## S3 Bucket Details

| Field             | Value                           |
| ----------------- | ------------------------------- |
| Bucket            | `s3://eonlabs-findings`         |
| Region            | `us-west-2`                     |
| Prefix            | `sessions/`                     |
| Credential Source | 1Password Claude Automation vault        |
| 1Password Item    | `ise47dxnkftmxopupffavsgby4`    |

---

## Troubleshooting

### "op: command not found"

Install 1Password CLI:

```bash
brew install 1password-cli
```

### "not signed in to 1Password"

Sign in:

```bash
op signin
```

### "vault not found" or access denied

Contact your admin to get access to the Claude Automation vault.

### "brotli: command not found"

Install Brotli:

```bash
brew install brotli
```

### AWS authentication errors

Verify your 1Password access:

```bash
op read "op://Claude Automation/ise47dxnkftmxopupffavsgby4/access key id"
```

If this fails, you don't have access to the credential item.

---

## Security Notes

- **Never commit credentials** to git
- Credentials are injected at runtime via 1Password
- S3 access requires Claude Automation vault membership
- Session files may contain sensitive conversation data

---

## Related Documentation

- [Session Chronicle SKILL.md](../SKILL.md)
- [S3 Sharing ADR](/docs/adr/2026-01-02-session-chronicle-s3-sharing.md)
- [Design Spec](/docs/design/2026-01-02-session-chronicle-s3-sharing/spec.md)
