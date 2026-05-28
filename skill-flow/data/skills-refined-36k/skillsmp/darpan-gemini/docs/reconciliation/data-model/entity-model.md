# Reconciliation Configuration Entity Model

This document maps the reconciliation configuration entities to their Moqui definitions in this repo.
The model focuses on configuration and definition storage only. Execution, auditing, and result storage
are intentionally out of scope.

## Source of Truth (Code)

- Reconciliation entities: `runtime/component/darpan/entity/ReconciliationEntities.xml`
- Mapping entities: `runtime/component/darpan/entity/MappingEntities.xml`
- Party entities: `runtime/component/darpan/entity/PartyEntities.xml`
- DataDocument: `framework/entity/EntityEntities.xml`
- SystemMessageRemote: `framework/entity/ServiceEntities.xml`
- Enumeration: `framework/entity/BasicEntities.xml`

## Entity Relationship Diagram

```mermaid
erDiagram

    RECONCILIATION ||--o{ RECONCILIATION_RUN : groups
    PARTY ||--o{ RECONCILIATION : owns

    RECONCILIATION_RUN ||--o{ RUN_DATA_DOCUMENT : uses
    DATA_DOCUMENT ||--o{ RUN_DATA_DOCUMENT : defined_by

    RECONCILIATION_RUN ||--o{ RUN_SYSTEM_INSTANCE : runs_on
    SYSTEM_MESSAGE_REMOTE ||--o{ RUN_SYSTEM_INSTANCE : provides_data

    RULE_SET ||--o{ RULE : contains
    RULE_SET ||--o{ RECONCILIATION_RUN : concludes_with

    RECONCILIATION_MAPPING ||--o{ RECONCILIATION_MAPPING_MEMBER : defines
    ENUMERATION ||--o{ RECONCILIATION_MAPPING_MEMBER : identifies_system


    RECONCILIATION {
        string reconciliation_id PK
        string reconciliation_name
        string description
        string schedule_expr
        string party_id FK
        boolean is_active
    }

    RECONCILIATION_RUN {
        string reconciliation_run_id PK
        string reconciliation_id FK
        string run_name
        string data_domain
        string purpose
        string default_time_window
        string ruleset_id FK
        int run_sequence
    }

    PARTY {
        string party_id PK
        string party_type
        string party_name
    }

    DATA_DOCUMENT {
        string data_document_id PK
        string data_document_name
        string primary_entity_name
        string description
    }

    RUN_DATA_DOCUMENT {
        string reconciliation_run_id FK
        string data_document_id FK
        string filter_expression
        string aggregation
        boolean is_required
    }

    SYSTEM_MESSAGE_REMOTE {
        string system_message_remote_id PK
        string remote_system_type
        string remote_system_name
        string environment
    }

    RUN_SYSTEM_INSTANCE {
        string reconciliation_run_id FK
        string system_message_remote_id FK
        string role
    }

    RULE_SET {
        string ruleset_id PK
        string name
        string version
    }

    RULE {
        string rule_id PK
        string ruleset_id FK
        string rule_type
        string expression
        string severity
    }

    RECONCILIATION_MAPPING {
        string reconciliation_mapping_id PK
        string mapping_name
        string description
        datetime created_date
        datetime last_updated_date
    }

    RECONCILIATION_MAPPING_MEMBER {
        string mapping_member_id PK
        string reconciliation_mapping_id FK
        string system_enum_id FK
        string system_field_name
        datetime created_date
    }

    ENUMERATION {
        string enum_id PK
        string enum_type_id
        string enum_code
        string description
    }
```

**Note**
- The diagram uses snake_case field names for readability.
- Source-of-truth field names live in the entity XML files linked above.

## Model Goals

- Define what should be reconciled, not how
- Enable reusable reconciliation runs across clients
- Leverage Moqui-native entities wherever possible
- Keep configuration declarative and schedulable

## Core Entities

### Reconciliation (darpan.reconciliation.Reconciliation)
A schedulable parent entity that groups one or more reconciliation runs.

**Purpose**
- Acts as the orchestration boundary
- Defines scheduling cadence
- Scoped to a client via `darpan.party.Party`

**Key Fields**
- `reconciliationId`
- `reconciliationName`
- `description`
- `scheduleExpr`
- `partyId`
- `isActive`

### ReconciliationRun (darpan.reconciliation.ReconciliationRun)
Defines a single reconciliation check within a reconciliation.

**Purpose**
- Represents one atomic comparison or validation
- Executed as part of a reconciliation group
- Reusable across clients if needed

**Key Fields**
- `reconciliationRunId`
- `reconciliationId`
- `runName`
- `dataDomain` (orders, returns, shipments)
- `purpose` (createdSync, statusMatch, financialMatch)
- `defaultTimeWindow`
- `ruleSetId`
- `runSequence`

### Party (darpan.party.Party)
Represents the client, merchant, or tenant.

**Purpose**
- Multi-tenant isolation
- Ownership of reconciliation configurations

**Key Fields**
- `partyId`
- `partyTypeId`
- `partyName`

### DataDocument (moqui.entity.document.DataDocument)
Defines a canonical data point used in reconciliation.

**Purpose**
- Reusable metric definitions
- Source-agnostic representation of data

**Examples**
- Order count
- Total order amount
- Shipment count by status

**Key Fields**
- `dataDocumentId`
- `documentName`
- `primaryEntityName`

### RunDataDocument (darpan.reconciliation.RunDataDocument)
Associates DataDocuments with a ReconciliationRun.

**Purpose**
- Applies run-specific filters and aggregations
- Controls which metrics are mandatory

**Key Fields**
- `reconciliationRunId`
- `dataDocumentId`
- `filterExpression`
- `aggregation`
- `isRequired`

### SystemMessageRemote (moqui.service.message.SystemMessageRemote)
Represents an external or internal system instance.

**Purpose**
- Defines where data is sourced from
- Encapsulates integration details

**Examples**
- Shopify (Prod)
- OFBiz (Stage)
- NetSuite (Prod)

**Key Fields**
- `systemMessageRemoteId`
- `description`
- `sendUrl`
- `receiveUrl`
- `messageAuthEnumId`

### RunSystemInstance (darpan.reconciliation.RunSystemInstance)
Associates systems with a reconciliation run.

**Purpose**
- Defines the role of each system in a run
- Supports source, target, or peer comparisons

**Key Fields**
- `reconciliationRunId`
- `systemMessageRemoteId`
- `role`

### RuleSet and Rule (darpan.reconciliation.RuleSet, darpan.reconciliation.Rule)
Defines conclusion logic for reconciliation runs.

**Purpose**
- Determines success, warnings, or failures
- Encapsulates business tolerances and thresholds

**RuleSet Key Fields**
- `ruleSetId`
- `name`
- `version`

**Rule Key Fields**
- `ruleId`
- `ruleSetId`
- `ruleType`
- `expression`
- `severity`

### ReconciliationMapping (darpan.mapping.ReconciliationMapping)
Defines a named mapping set for reconciliation system fields.

**Purpose**
- Groups mapping entries under a stable name

**Key Fields**
- `reconciliationMappingId`
- `mappingName`
- `description`
- `createdDate`
- `lastUpdatedDate`

### ReconciliationMappingMember (darpan.mapping.ReconciliationMappingMember)
Stores a single mapping entry tied to a mapping and system enum.

**Purpose**
- Captures system-specific field names
- Enables field-level mapping by system

**Key Fields**
- `mappingMemberId`
- `reconciliationMappingId`
- `systemEnumId` (from `moqui.basic.Enumeration`)
- `systemFieldName`
- `createdDate`

## What Is Out of Scope (By Design)

- Execution tracking
- Data pull results
- Rule evaluation outcomes
- Alerts and notifications

These concerns will be introduced in a separate execution-layer model.

## Future Enhancements

- Execution entities (`ReconciliationExecution`, `RunExecution`)
- Rule evaluation result storage
- Alerting and notification hooks
- Moqui entity XML generation
