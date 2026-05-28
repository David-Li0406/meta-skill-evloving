---
date: 2026-01-20
title: K3s cluster unreachable after OPNsense firewall rule change
severity: moderate
duration: 1h 45m
systems: [k3s, opnsense, networking]
tags: [kubernetes, networking, firewall]
commit: https://github.com/ammar/infra/commit/a1b2c3d
---

## Summary

K3s API server became unreachable from workstation after applying new firewall rules to OPNsense. Cluster workloads continued running but couldn't be managed. Resolved by correcting VLAN interface assignment in firewall rule.

## Timeline

- **14:15** - Applied new firewall ruleset via Terraform to restrict inter-VLAN traffic
- **14:18** - Noticed `kubectl` commands timing out
- **14:20** - Verified cluster nodes still running via Proxmox console
- **14:25** - Started checking OPNsense logs, saw blocked traffic from workstation VLAN to server VLAN
- **14:45** - Identified that new rule was applied to wrong interface (LAN instead of SERVER_VLAN)
- **15:00** - Corrected interface assignment, tested
- **15:05** - Verified full connectivity restored

## What Happened

I was tightening firewall rules to better segment the network - specifically blocking IoT VLAN from reaching server VLAN except for specific allowed services. The Terraform config looked correct, but I had the interface names wrong in my mental model.

OPNsense interface names (opt1, opt2, etc.) don't match the VLAN names I assigned in the UI. The rule that was supposed to apply to IoT→Server traffic actually applied to Workstation→Server traffic because I assumed opt1 was IoT when it was actually the workstation VLAN.

Traffic was being silently dropped. The cluster kept running because the nodes could still talk to each other (same VLAN), but I couldn't reach the API server from my workstation.

## Contributing Factors

- OPNsense interface naming is confusing - UI names don't match API/Terraform names
- No validation that Terraform changes matched intent before applying
- Applied change without a test that would immediately catch connectivity loss
- Didn't have interface mapping documented anywhere

## What I Was Wrong About

I assumed I knew which interface was which based on the order I created them. I had a mental model of "opt1 = first VLAN I made = IoT" but OPNsense doesn't number them that way. I'd never actually verified this mapping.

More broadly, I was treating firewall rule changes as low-risk because "I can always roll back." But the failure mode here was silent - traffic just dropped, no alert, no error in Terraform.

## What Helped

- Proxmox console access let me verify the cluster was actually healthy
- OPNsense logs clearly showed the blocked traffic once I looked
- Having Terraform state meant I could see exactly what changed

## What Could Have Been Worse

- If I'd made this change before leaving for a trip, the cluster would have been unmanageable remotely
- If the rule had blocked inter-node traffic (not just workstation→cluster), the cluster itself would have failed
- No alerting would have caught this - I only noticed because I tried to use kubectl

## Is This a Pattern?

- [ ] One-off: Correct and move on
- [x] Pattern: Revisit the approach

This is the second time I've been bitten by not understanding OPNsense's interface naming. The approach of "just remember which interface is which" doesn't scale. Need to either:
- Document the mapping definitively
- Use Terraform data sources to look up interface by description rather than hardcoding names
- Add smoke tests after firewall changes

## Action Items

- [x] Document OPNsense interface mapping in infra repo README
- [ ] Add post-apply smoke test to Terraform workflow that verifies basic connectivity
- [ ] Set up alerting for kubectl API server unreachable (even just a simple cron job)

## Lessons

- OPNsense opt1/opt2/etc names are assigned in creation order of *interfaces*, not VLANs
- Firewall changes that block traffic fail silently from Terraform's perspective
- "I can roll back" isn't a safety net if you don't notice the failure
- For firewall changes, have a connectivity test ready to run immediately after apply
