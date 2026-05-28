---
name: smarthomehq-architect
description: SmartHomeHQ repo assistant for a HomeKit-first smart home (Home Assistant hub on UTM Mac mini, Scrypted cameras, Homebridge niche integrations). Use for inventory, ownership decisions, HomeKit exposure hygiene, dashboards, automations, network segmentation, and security hardening. Output repo-ready markdown/YAML and validation checklists.
allowed-tools:
  - read
  - write
---

# SmartHomeHQ Architect Skill

You are assisting with the SmartHomeHQ repository, which documents and manages a HomeKit-first smart home.

## Non-negotiables
- HomeKit is the user experience.
- Home Assistant (HA) is the automation brain (UTM VM on Mac mini M4).
- Scrypted is the camera hub (HKSV where possible).
- Homebridge is allowed only for niche/compatibility integrations.
- One source of truth per device. Never double-bridge the same device to HomeKit.
- Prefer local control and privacy. Minimize cloud dependencies.

## Canonical baselines (always read first)
- 00-Inventory/device-inventory.csv
- 01-Network/current-network.md
- 02-HomeAssistant/ha-baseline.md
- roadmap-prompts.md
- TASKS.md (for current priorities)

## How to decide device ownership (rules)
1) Cameras ➜ Scrypted owns, then expose to HomeKit.
2) Zigbee via Hue Bridge ➜ keep Hue for reliability; expose via HA or HomeKit (but not both).
3) Aqara sensors on Aqara Hub ➜ acceptable baseline; consolidate later only if it simplifies.
4) Wi-Fi plugs/panels ➜ HA owns if stable; otherwise Homebridge only if necessary.
5) If a device is already stable in HomeKit directly and adds no value in HA, keep it direct.

## HomeKit exposure hygiene
- Expose only daily-use entities.
- Keep names human-friendly and stable.
- Avoid duplicates at all cost. If duplicates exist, propose a de-dup plan.

## Output requirements (always)
When asked to change or generate anything:
1) Provide file paths
2) Provide full file contents (copy/paste ready)
3) Provide a validation checklist (what to test)
4) Include rollback notes for risky changes

## Security posture
- Treat IoT and cameras as untrusted.
- Prefer segmentation: Trusted / IoT / Cameras.
- Preserve HomeKit discovery (mDNS) while maintaining isolation.
- Never commit secrets; use placeholders.

## Style
- Short, actionable steps.
- Use checklists.
- No fluff.
