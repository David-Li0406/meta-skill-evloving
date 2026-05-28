# Drools for Configurable Reconciliation Logic

## Goal

Keep reconciliation logic configurable per client while the execution service stays generic and stable.

## Why Drools

- Externalizes rules from application code
- Supports DRL and decision tables for business-friendly updates
- Separates facts (data) from rules (logic)
- Provides priorities and conditional execution for complex comparisons

## How It Fits the Platform

1. The service loads canonical facts (orders, shipments, payments, etc.)
2. It selects the rule package for the client and entity
3. Drools evaluates rules
4. Results are persisted in the reconciliation store

Only the rules change; the execution pipeline does not.

## Current Repo State

- RuleSet and Rule configuration entities live in `runtime/component/darpan/entity/ReconciliationEntities.xml`
- No Drools integration code is present yet in this component

## Operational Considerations

- Governance: versioned rule sets with review and approval
- Performance: batch execution and bounded fact sizes

## Next Steps

- Prototype the order presence rule in Drools
- Define the canonical fact model
- Pick the initial authoring format (DRL or decision tables)
