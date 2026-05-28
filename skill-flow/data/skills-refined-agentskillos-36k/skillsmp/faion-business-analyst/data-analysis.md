---
id: data-analysis
name: "Data Analysis"
domain: BA
skill: faion-business-analyst
category: "business-analysis"
---

# Data Analysis

## Metadata
- **Category:** BA Framework / Requirements Analysis and Design Definition
- **Difficulty:** Intermediate
- **Tags:** #methodology #babok #data #analysis #business-analysis
- **Agent:** faion-ba-agent

---

## Problem

Data exists in multiple systems with different definitions. Reports show conflicting numbers. Nobody understands what data the business needs. Systems are built without proper data design. Data quality issues cause ongoing problems.

Without data analysis:
- Inconsistent data definitions
- Poor data quality
- Missing data requirements
- Integration failures

---

## Framework

### What is Data Analysis?

Data Analysis in BA context examines:
- What data the business needs
- How data is structured
- Where data comes from and goes
- Data quality requirements
- Data relationships

### Data Analysis Components

```
Data Requirements → Data Modeling → Data Quality → Data Governance
```

### Step 1: Identify Data Needs

Determine what data is required:

| Question | Purpose |
|----------|---------|
| What information do users need? | Reports, screens |
| What data is captured? | Input data |
| What data is calculated? | Derived data |
| What data is stored? | Persistent data |
| What data is shared? | Integration data |

### Step 2: Define Data Elements

Document each data element:

| Attribute | Description |
|-----------|-------------|
| **Name** | Clear, unique name |
| **Definition** | Business meaning |
| **Type** | Text, number, date, etc. |
| **Format** | Specific format rules |
| **Values** | Valid values or ranges |
| **Source** | Where data comes from |
| **Owner** | Who is responsible |

### Step 3: Create Data Model

Visualize data structure:

**Conceptual model:** High-level entities and relationships
**Logical model:** Detailed attributes and relationships
**Physical model:** Technical implementation

### Step 4: Analyze Data Quality

Assess current data:

| Dimension | Description | Measure |
|-----------|-------------|---------|
| **Accuracy** | Correct values | Error rate |
| **Completeness** | All required data present | Missing value % |
| **Consistency** | Same across systems | Conflict count |
| **Timeliness** | Current and available | Age of data |
| **Validity** | Conforms to rules | Invalid value % |
| **Uniqueness** | No duplicates | Duplicate rate |

### Step 5: Define Data Rules

Business rules for data:

| Rule Type | Example |
|-----------|---------|
| **Validation** | Email must contain @ |
| **Derivation** | Total = Quantity x Price |
| **Default** | Status defaults to "New" |
| **Constraint** | Start date before end date |
| **Uniqueness** | Customer ID is unique |

---

## Templates

### Data Dictionary Template

```markdown
# Data Dictionary: [System/Domain Name]

**Version:** [X.X]
**Date:** [Date]
**Author:** [Name]

## Entity: [Entity Name]

**Description:** [What this entity represents]
**Owner:** [Data owner]
**Source:** [Where data originates]

### Attributes

| Name | Definition | Type | Format | Required | Valid Values | Rules |
|------|------------|------|--------|----------|--------------|-------|
| [Name] | [Definition] | [Type] | [Format] | Y/N | [Values] | [Rules] |

### Example Records

| [Attr 1] | [Attr 2] | [Attr 3] |
|----------|----------|----------|
| [Value] | [Value] | [Value] |

### Relationships

| Related Entity | Relationship | Cardinality |
|----------------|--------------|-------------|
| [Entity] | [Type] | [1:1, 1:N, N:N] |

### Business Rules

| Rule ID | Rule Description |
|---------|------------------|
| DR-01 | [Rule] |
```

### Data Requirements Template

```markdown
# Data Requirements: [Feature/Project Name]

**Version:** [X.X]
**Date:** [Date]
**Analyst:** [Name]

## Data Overview

### Purpose
[What data supports and why]

### Data Entities

| Entity | Description | Source | New/Existing |
|--------|-------------|--------|--------------|
| [Entity] | [Description] | [Source] | New/Existing |

## Detailed Requirements

### [Entity 1]: [Name]

**Description:** [Business description]

**Attributes:**

| Attribute | Type | Size | Required | Description | Validation |
|-----------|------|------|----------|-------------|------------|
| [Name] | [Type] | [Size] | Y/N | [Description] | [Rules] |

**Derived Data:**

| Attribute | Formula | Source Attributes |
|-----------|---------|-------------------|
| [Name] | [Formula] | [Sources] |

## Data Quality Requirements

| Entity | Quality Rule | Threshold |
|--------|--------------|-----------|
| [Entity] | [Rule] | [Threshold] |

## Data Volumes

| Entity | Current | Expected (1yr) | Expected (3yr) |
|--------|---------|----------------|----------------|
| [Entity] | [Count] | [Count] | [Count] |

## Data Integration

| Source System | Target System | Data | Frequency | Method |
|---------------|---------------|------|-----------|--------|
| [System] | [System] | [Data] | [Freq] | [Method] |

## Data Security

| Entity | Classification | Access Rules |
|--------|----------------|--------------|
| [Entity] | [Public/Internal/Confidential] | [Rules] |
```

### Data Quality Assessment Template

```markdown
# Data Quality Assessment: [Data Domain]

**Date:** [Date]
**Assessor:** [Name]
**Data Source:** [Source]
**Sample Size:** [N records]

## Quality Dimensions

### Accuracy
- **Metric:** Error rate
- **Finding:** [X%] of records have errors
- **Examples:** [Examples of errors]

### Completeness
- **Metric:** Missing values
- **Finding:** [Field X] has [Y%] null values
- **Impact:** [Impact of missing data]

### Consistency
- **Metric:** Cross-system matches
- **Finding:** [X%] records match between systems
- **Discrepancies:** [Types of inconsistencies]

### Timeliness
- **Metric:** Data age
- **Finding:** Average data age is [X days]
- **Impact:** [Impact of stale data]

### Validity
- **Metric:** Rule violations
- **Finding:** [X%] records violate business rules
- **Violations:** [Types of violations]

### Uniqueness
- **Metric:** Duplicate rate
- **Finding:** [X%] duplicate records
- **Impact:** [Impact of duplicates]

## Summary

| Dimension | Score (1-5) | Status | Priority |
|-----------|-------------|--------|----------|
| Accuracy | [X] | Green/Yellow/Red | H/M/L |
| Completeness | [X] | Green/Yellow/Red | H/M/L |
| Consistency | [X] | Green/Yellow/Red | H/M/L |
| Timeliness | [X] | Green/Yellow/Red | H/M/L |
| Validity | [X] | Green/Yellow/Red | H/M/L |
| Uniqueness | [X] | Green/Yellow/Red | H/M/L |

## Recommendations

| Issue | Recommendation | Priority | Effort |
|-------|----------------|----------|--------|
| [Issue] | [Recommendation] | H/M/L | H/M/L |
```

---

## Examples

### Example 1: Customer Entity

**Entity:** Customer

| Attribute | Type | Required | Validation |
|-----------|------|----------|------------|
| CustomerID | Integer | Yes | Auto-generated, unique |
| FirstName | Text(50) | Yes | Not empty |
| LastName | Text(50) | Yes | Not empty |
| Email | Text(100) | Yes | Valid email format |
| Phone | Text(20) | No | Valid phone format |
| Status | Text(10) | Yes | Active, Inactive, Prospect |
| CreatedDate | DateTime | Yes | Auto-set on creation |

**Business Rules:**
- DR-01: CustomerID is system-generated and immutable
- DR-02: Email must be unique across all customers
- DR-03: Status defaults to "Prospect" for new customers

### Example 2: Data Quality Findings

**Assessment of Product Data:**

| Dimension | Score | Findings |
|-----------|-------|----------|
| Accuracy | 3/5 | 8% of prices incorrect vs. catalog |
| Completeness | 4/5 | 2% missing descriptions |
| Consistency | 2/5 | Product names differ across systems |
| Timeliness | 5/5 | Updated daily, acceptable |
| Validity | 4/5 | 1% with invalid category codes |
| Uniqueness | 3/5 | 5% duplicate SKUs |

**Priority Issue:** Consistency - product naming convention needed

---

## Common Mistakes

1. **No data dictionary** - Everyone defines data differently
2. **Skipping data quality** - Assuming data is correct
3. **Technical only** - Missing business definitions
4. **No ownership** - Nobody responsible for data
5. **Ignoring history** - How will data change over time?

---

## Data Modeling Levels

| Level | Purpose | Audience |
|-------|---------|----------|
| **Conceptual** | What entities and relationships | Business stakeholders |
| **Logical** | Detailed attributes and rules | BA, developers |
| **Physical** | Tables, columns, indexes | Database developers |

---

## Entity Relationship Notation

| Symbol | Meaning |
|--------|---------|
| Rectangle | Entity |
| Line | Relationship |
| 1 | One |
| N or * | Many |
| ○ | Optional |
| | | Mandatory |

Example: Customer 1 ----< N Order (One customer has many orders)

---

## Next Steps

After data analysis:
1. Create data dictionary
2. Validate with stakeholders
3. Assess data quality
4. Define data migration needs
5. Connect to Decision Analysis methodology

---

## References

- BA Framework Guide v3 - Requirements Analysis and Design Definition
- BA industry Data Analysis Guidelines
