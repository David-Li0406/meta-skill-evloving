# PLAYBOOK.standard.md — Operational Playbook Standard

## Purpose

Playbooks are for **doing**, not discussing. They are operational runbooks: incident response, maintenance routines, release steps, emergency procedures.

## Audience

* On-call engineers
* Operators / maintainers
* Anyone executing time-sensitive procedures

## Source of truth

* Real operational practice
* Verified commands and system capabilities

## Required sections

1. **When to use this**

   * trigger conditions and symptoms
2. **Do not use this when**

   * misfires and related playbooks
3. **Prerequisites**

   * access, permissions, tools
4. **Risk level**

   * Low | Medium | High + what can go wrong
5. **Checklist**

   * quick overview of steps
6. **Procedure (step-by-step)**

   * numbered steps with expected outputs
7. **Verification**

   * how to confirm resolution
8. **Rollback / Fallback**

   * how to safely undo or mitigate
9. **Escalation**

   * who/where to escalate
10. **Postmortem notes**

    * what to capture for follow-up

## Style rules

* No ambiguity. No “maybe.” Use explicit conditions.
* Put critical warnings in bold.
* Prefer copy-pastable commands with placeholders.

## Allowed content

* Links to dashboards, logs, metrics (if available)
* Short rationale if it prevents mistakes

## Forbidden content

* Architectural debate (SPEC/ADR)
* Long onboarding tutorials (Guides)

## Maintenance rules

* Validate playbooks regularly.
* Remove or update steps that no longer work.
* Keep escalation paths current.

## Quality checklist

* A medium-context engineer can execute without improvising.
* Rollback exists for risky operations.
* Verification steps exist.

## Common failure modes

* Missing rollback
* Steps depend on tribal knowledge
* Unverified commands
