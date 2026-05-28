# Trading Psychology - Validations

## Pre-Trade Checklist Exists

### **Id**
check-pre-trade-checklist
### **Description**
Trading systems should include pre-trade emotional check
### **Pattern**
trade|entry|position
### **File Glob**
**/*.{py,js,ts}
### **Match**
present
### **Context Pattern**
checklist|emotional|state|assessment
### **Message**
Include pre-trade emotional state assessment
### **Severity**
warning
### **Autofix**


## Trade Journaling Implementation

### **Id**
check-journal-logging
### **Description**
Trades should be logged with psychological notes
### **Pattern**
trade|order|execute
### **File Glob**
**/*.{py,js,ts}
### **Match**
present
### **Context Pattern**
journal|log|record|note
### **Message**
Implement trade journaling for psychological analysis
### **Severity**
info
### **Autofix**


## Daily Loss Limits

### **Id**
check-daily-limits
### **Description**
Trading systems should enforce daily loss limits
### **Pattern**
daily.*limit|max.*loss|stop.*trading
### **File Glob**
**/*.{py,js,ts}
### **Match**
absent
### **Context Pattern**
trade|strategy
### **Message**
Implement daily loss limits to prevent tilt
### **Severity**
warning
### **Autofix**


## Post-Loss Cooldown

### **Id**
check-cooldown-period
### **Description**
Systems should enforce cooldown after losses
### **Pattern**
cooldown|wait|break|pause
### **File Glob**
**/*.{py,js,ts}
### **Match**
absent
### **Context Pattern**
loss|after.*trade
### **Message**
Implement mandatory cooldown period after losses
### **Severity**
info
### **Autofix**


## Maximum Trades Per Day

### **Id**
check-max-trades
### **Description**
Limit number of trades to prevent overtrading
### **Pattern**
max.*trades|trade.*limit|trades.*per.*day
### **File Glob**
**/*.{py,js,ts}
### **Match**
absent
### **Context Pattern**
daily|session
### **Message**
Implement maximum trades per day limit
### **Severity**
info
### **Autofix**


## Position Size Rules

### **Id**
check-size-rules
### **Description**
Size should be systematic, not emotional
### **Pattern**
position.*size|size.*calc
### **File Glob**
**/*.{py,js,ts}
### **Match**
present
### **Context Pattern**
system|rule|formula
### **Message**
Use systematic position sizing, not discretionary
### **Severity**
warning
### **Autofix**


## Stop Loss Immutability

### **Id**
check-stop-immutable
### **Description**
Stops should not be moveable after entry
### **Pattern**
move.*stop|change.*stop|widen.*stop
### **File Glob**
**/*.{py,js,ts}
### **Match**
present
### **Message**
Warning: Moving stops is a common psychological trap
### **Severity**
warning
### **Autofix**


## Tilt Detection System

### **Id**
check-tilt-detection
### **Description**
Implement automated tilt detection
### **Pattern**
tilt|consecutive.*loss|revenge
### **File Glob**
**/*.{py,js,ts}
### **Match**
absent
### **Context Pattern**
detect|monitor|track
### **Message**
Implement tilt detection to prevent spiral losses
### **Severity**
info
### **Autofix**
