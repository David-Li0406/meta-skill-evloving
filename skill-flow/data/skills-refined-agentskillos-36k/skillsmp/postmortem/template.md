---
date: YYYY-MM-DD
title: Brief description of the incident
severity: minor | moderate | major
duration: Xh Ym
systems: [list, of, affected, systems]
tags: [nixos, kubernetes, networking, storage, etc.]
commit: https://github.com/username/repo/commit/abc123
---

## Summary

One or two sentences: what broke, how long it was broken, what was affected.

## Timeline

All times in UTC (or your local timezone, be consistent).

- **HH:MM** - First indication of problem
- **HH:MM** - Investigation began
- **HH:MM** - Key discovery or action
- **HH:MM** - Resolution applied
- **HH:MM** - Confirmed resolved

## What Happened

Narrative description of the sequence of events. Focus on what the situation looked like at each stage, what information was available, and what decisions were made based on that information.

## Contributing Factors

What conditions combined to cause this incident? List all that apply - there's rarely a single cause.

-
-
-

## What I Was Wrong About

What assumptions, mental models, or expectations turned out to be incorrect? This is often more valuable than the fix itself.

-

## What Helped

What limited the impact or made debugging easier? Worth noting so you can rely on these in the future.

-

## What Could Have Been Worse

Near-misses: things that could have made this much worse but didn't happen. These reveal risks that haven't materialized yet.

-

## Is This a Pattern?

Is this a one-off mistake, or does it suggest something about the approach needs to change?

- [ ] One-off: Correct and move on
- [ ] Pattern: Revisit the approach

If pattern, what needs to change at a higher level?

## Action Items

Specific, bounded actions. Each should be completable and verifiable.

- [ ] Action item with clear scope
- [ ] Another action item

## Lessons

Key takeaways. What would you tell past-you? What should you check first next time you see similar symptoms?

-
