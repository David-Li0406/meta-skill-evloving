---
name: audit-vibe-check
description: Autonomously verifying venue "Buzz" status and frontend rendering.
---

# Audit Vibe Check

This skill allows the agent to autonomous verify that the "Vibe" system is working end-to-end, from the database state to the visual frontend.

## Capabilities
- **Data Discovery**: Finds a venue that should be "Buzzing" (high vibe score).
- **Visual Verification**: Uses the browser to confirm the "Gold Pin" and "Pulse Animation" are visible.

## Usage

### 1. Run Verification Script
Execute the helper script to find a target and perform the visual check (simulated or via browser tool).

```bash
npx tsx scripts/verify-vibe.ts
```

### 2. Manual/Agentic Verification
If the script identifies a target URL but cannot self-verify (e.g. headless environment), the agent should:
1. Open the Browser Tool.
2. Navigate to the `targetUrl`.
3. Assert that the element `.marker-gold` exists.
4. Assert that the element `.animate-pulse` exists.

## Success Criteria
- [ ] Database has at least one 'buzzing' venue.
- [ ] Frontend displays the Gold Pin for that venue.
