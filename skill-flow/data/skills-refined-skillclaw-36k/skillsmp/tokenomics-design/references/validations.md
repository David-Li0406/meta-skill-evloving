# Tokenomics Design - Validations

## Allocation Totals 100%

### **Id**
check-total-allocation
### **Description**
Verify all allocations sum to 100%
### **Pattern**
allocation|distribution
### **File Glob**
**/tokenomics*.{md,yaml,json}
### **Match**
present
### **Message**
Verify all token allocations sum to exactly 100%
### **Severity**
error
### **Autofix**


## Vesting Schedule Defined

### **Id**
check-vesting-schedule
### **Description**
All allocations should have vesting terms
### **Pattern**
vest|cliff|unlock|TGE
### **File Glob**
**/tokenomics*.{md,yaml,json}
### **Match**
absent_in_context
### **Context Pattern**
team|investor|advisor
### **Message**
Define vesting schedule for insider allocations
### **Severity**
error
### **Autofix**


## Minimum Cliff Duration

### **Id**
check-cliff-duration
### **Description**
Insider allocations should have meaningful cliff
### **Pattern**
cliff.*[0-3]\s*month|no.*cliff
### **File Glob**
**/tokenomics*.{md,yaml,json}
### **Match**
present
### **Message**
Consider longer cliff (6-12 months) for better alignment
### **Severity**
warning
### **Autofix**


## TGE Unlock Percentage

### **Id**
check-tge-percentage
### **Description**
Check TGE unlock isn't too high for insiders
### **Pattern**
TGE.*[2-5][0-9]%|unlock.*[2-5][0-9]%.*TGE
### **File Glob**
**/tokenomics*.{md,yaml,json}
### **Match**
present
### **Message**
TGE unlock above 20% for insiders may cause dump pressure
### **Severity**
warning
### **Autofix**


## Emission Schedule Defined

### **Id**
check-emission-schedule
### **Description**
Token emissions should have clear schedule
### **Pattern**
emission|inflation|reward.*rate
### **File Glob**
**/tokenomics*.{md,yaml,json}
### **Match**
absent_in_context
### **Context Pattern**
schedule|rate|yearly|monthly
### **Message**
Define clear emission schedule with rates and duration
### **Severity**
warning
### **Autofix**


## Token Utility Specified

### **Id**
check-utility-defined
### **Description**
Token should have clear utility
### **Pattern**
utility|use.*case|purpose
### **File Glob**
**/tokenomics*.{md,yaml,json}
### **Match**
absent
### **Message**
Define clear token utility beyond speculation
### **Severity**
warning
### **Autofix**


## Value Accrual Mechanism

### **Id**
check-value-accrual
### **Description**
Token should capture protocol value
### **Pattern**
fee.*shar|buyback|burn|revenue
### **File Glob**
**/tokenomics*.{md,yaml,json}
### **Match**
absent
### **Message**
Consider value accrual mechanism (fees, burns, etc.)
### **Severity**
info
### **Autofix**


## Governance Security

### **Id**
check-governance-safeguards
### **Description**
Governance tokens need safeguards
### **Pattern**
governance|voting|proposal
### **File Glob**
**/tokenomics*.{md,yaml,json}
### **Match**
present
### **Context Pattern**
timelock|delay|quorum|veto
### **Message**
Add governance safeguards (timelock, quorum, etc.)
### **Severity**
warning
### **Autofix**


## Supply Cap or Emission End

### **Id**
check-supply-cap
### **Description**
Token should have supply cap or decreasing emissions
### **Pattern**
uncapped|unlimited|infinite
### **File Glob**
**/tokenomics*.{md,yaml,json}
### **Match**
present
### **Message**
Consider supply cap or decreasing emission schedule
### **Severity**
warning
### **Autofix**


## Liquidity Provision Plan

### **Id**
check-liquidity-plan
### **Description**
Define how liquidity will be provided
### **Pattern**
liquidity|lp|amm|trading
### **File Glob**
**/tokenomics*.{md,yaml,json}
### **Match**
absent
### **Message**
Define liquidity provision strategy
### **Severity**
info
### **Autofix**
