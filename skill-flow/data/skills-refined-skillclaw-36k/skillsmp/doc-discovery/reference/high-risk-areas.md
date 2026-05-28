# High-Risk Areas Guide

When a task touches these areas, load specialized documentation.

## Auth/RLS/Permissions

**Load**: Auth patterns doc, RLS policies documentation

**Key concerns**:
- RLS policies must be checked before any table access
- `createAdminClient()` usage must be documented
- Permission changes can break user access

**Questions to answer**:
- What RLS policies exist on affected tables?
- Does this change require admin client?
- What permission levels are involved?

## AI/Prompts/Context

**Load**: AI context assembly docs, embedding documentation

**Key concerns**:
- Context window limits must be respected
- Prompt changes affect all AI interactions
- Embeddings regeneration may be required

**Questions to answer**:
- What context is assembled for this AI feature?
- Will prompt changes affect other features?
- Are embeddings affected?

## Billing/Credits/Entitlements

**Load**: Stripe integration docs, entitlement rules

**Key concerns**:
- Credit accrual must be accurate
- Entitlement checks gate feature access
- Payment flows are production-critical

**Questions to answer**:
- How are credits/entitlements checked?
- What Stripe webhooks are involved?
- What happens on failed payment?

## Schema/Migrations

**Load**: Migration safety guide, schema documentation

**Key concerns**:
- Migrations must be reversible
- Production SQL must be provided
- Data integrity must be preserved

**Questions to answer**:
- Is migration backwards-compatible?
- What's the rollback plan?
- Are there data dependencies?
