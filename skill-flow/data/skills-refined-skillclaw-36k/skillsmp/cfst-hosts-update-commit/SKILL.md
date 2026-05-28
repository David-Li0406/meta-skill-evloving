---
name: cfst-hosts-update-commit
description: Run the WorkerVless2sub cfst_hosts.sh workflow to refresh result_hosts.txt and nowip_hosts.txt, then stage and commit those updates in git. Use when asked to update CloudflareST hosts/IPs, run the speed test, or auto-commit the refreshed results for this repo.
---

# Cfst Hosts Update Commit

## Overview

Run the repo's cfst_hosts.sh workflow to pick the fastest IP, update result_hosts.txt and nowip_hosts.txt, and commit those file changes in git.

## Workflow

1. Confirm location and prerequisites
   - Work from the repo root containing cfst_hosts.sh and CloudflareST.
   - If this is the first run, be ready to input the current Cloudflare IP when prompted; it will be stored in nowip_hosts.txt.

2. Run the update script
   - Prefer sudo bash cfst_hosts.sh so /etc/hosts and /etc/hosts_backup can be updated.
   - If sudo is not allowed, run bash cfst_hosts.sh and note that /etc/hosts may not update.

3. Validate outputs
   - Ensure result_hosts.txt exists and has at least one data row (header + IP row).
   - Ensure nowip_hosts.txt contains the new IP selected from result_hosts.txt.

4. Stage and commit
   - Check git status -sb; only proceed if the intended changes are result_hosts.txt and nowip_hosts.txt.
   - Stage: git add result_hosts.txt nowip_hosts.txt.
   - Commit with a short, imperative message like "Update CFST hosts" (or user-specified).
   - Do not push unless explicitly asked.

## Failure handling

- If result_hosts.txt is missing or has no IP rows, stop and report; do not commit.
- If cfst_hosts.sh exits early (no IP found), do not commit.
- If unexpected files change, ask before committing.
