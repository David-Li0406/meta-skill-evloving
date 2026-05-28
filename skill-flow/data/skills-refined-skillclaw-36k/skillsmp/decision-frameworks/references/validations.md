# Decision Frameworks - Validations

## Missing Decision Owner

### **Id**
no-decision-owner
### **Severity**
high
### **Type**
conceptual
### **Check**
Every decision should have clear ownership
### **Message**
No one owns this decision.
### **Fix Action**
Assign one Accountable person per decision

## Undocumented Decision Criteria

### **Id**
no-criteria
### **Severity**
medium
### **Type**
conceptual
### **Check**
Decision criteria should be explicit
### **Message**
Deciding without clear criteria.
### **Fix Action**
Define and weight decision criteria before evaluating

## Decision Taking Too Long

### **Id**
analysis-paralysis
### **Severity**
medium
### **Type**
conceptual
### **Check**
Decisions should be time-boxed
### **Indicators**
  - Same decision discussed in multiple meetings
  - Requests for more analysis
### **Message**
Analysis paralysis detected.
### **Fix Action**
Set decision deadline and force decision

## Sunk Cost Influencing Decision

### **Id**
sunk-cost-reasoning
### **Severity**
high
### **Type**
conceptual
### **Check**
Past investment should not influence future decisions
### **Indicators**
  - References to previous investment
  - Reluctance to change despite evidence
### **Message**
Sunk cost fallacy detected.
### **Fix Action**
Reframe around future costs and benefits only

## Pseudo-Consensus

### **Id**
false-consensus
### **Severity**
medium
### **Type**
conceptual
### **Check**
Stakeholders should genuinely agree or explicitly disagree
### **Indicators**
  - Silence treated as agreement
  - Dissent not surfaced
### **Message**
Consensus may not be real.
### **Fix Action**
Actively solicit disagreement and document

## Decision Not Documented

### **Id**
undocumented-decision
### **Severity**
medium
### **Type**
conceptual
### **Check**
Important decisions should be recorded
### **Message**
Decision made but not documented.
### **Fix Action**
Create decision record with rationale and context