---
name: pda-design-playbook
description: Patterns for designing PDAs: seed strategy, collision avoidance, upgrade considerations, and bump handling. Use when creating or auditing PDAs.
---

# PDA Design Playbook

Role framing: You are a PDA strategist. Your goal is to design deterministic, safe PDA schemes that survive upgrades and user mistakes.

## Initial Assessment
- What entities need PDAs? (global state, user state, vaults, authorities)
- Are seeds user-controlled? Any variable-length or unbounded fields?
- Will PDAs be reused across versions/programs?
- Need for PDA as signer in CPI?

## Core Principles
- Stable seeds: prefer fixed prefixes + canonical ordering; hash long/variable inputs with hashv.
- Avoid secrets in seeds; treat seeds as public.
- Store bump where needed; derive on-chain, don’t trust client-provided bump without check.
- Upgrade safety: don't change seeds post-deploy unless versioned.
- Respect 32-byte seed limit and 16 seed count.

## Workflow
1) Define resource graph: identify each PDA purpose and lifetime.
2) Choose seeds
   - Prefix constant, entity keys, indices; hash dynamic strings.
   - Decide canonical ordering to avoid duplicates.
3) Bump strategy
   - Use Pubkey::find_program_address; store bump in account data or pass in and verify.
   - For signer CPIs, include seeds+bump; encapsulate in helper.
4) Versioning
   - If seed change needed, add ersion seed and migrate data; keep old PDAs readable or closed safely.
5) Documentation
   - Record seeds, bump location, and use cases; add to account table.
6) Testing
   - Collision tests using random inputs; ensure ind_program_address succeeds; signer CPIs succeed.

## Templates / Playbooks
- Seed recipe examples: [b"vault", mint]; [b"user", user, pool]; hashed: [b"note", hashv(user_input)].
- Bump helper snippet (Rust): let (pda, bump) = Pubkey::find_program_address(...); store bump in account struct.

## Common Failure Modes + Debugging
- Seed too long: hash variable data; watch UTF-8 length.
- Wrong bump used: verify bump in program; ignore client-provided bump unless checked.
- PDA reuse across programs causing collision assumptions: include program-specific prefix.
- CPI signer fails: ensure seeds array matches creation seeds and bump; order matters.

## Quality Bar / Validation
- Each PDA documented with seeds, bump strategy, and purpose.
- Seed inputs bounded and canonicalized; collisions tested.
- Signer use tested in CPI paths.
- Migration plan if seeds change.

## Output Format
Provide PDA catalog: purpose, seeds, bump location, signer usage, and tests required.

## Examples
- Simple: Config PDA [b"config"] storing admin + bump.
- Complex: Pool + user positions
  - Pool state [b"pool", mint_a, mint_b_sorted]; authority [b"authority", pool]; user position [b"position", pool, user]; hashed notes for receipts; bump stored in each account; CPI signer for token authority.