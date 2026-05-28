# Dao Governance - Validations

## Voting without snapshot mechanism

### **Id**
no-vote-snapshot
### **Severity**
error
### **Type**
regex
### **Pattern**
  - getVotes.*balanceOf|votingPower.*balanceOf
### **Message**
Voting power should use snapshots, not current balance (flash loan risk)
### **Fix Action**
Use ERC20Votes and getPastVotes() for snapshot-based voting
### **Applies To**
  - *.sol

## Governor without TimelockController

### **Id**
no-timelock
### **Severity**
error
### **Type**
regex
### **Pattern**
  - is\s+Governor(?!.*TimelockControl)
### **Message**
Governor should use TimelockController for execution delay
### **Fix Action**
Inherit GovernorTimelockControl and deploy with timelock
### **Applies To**
  - *.sol

## Timelock delay too short

### **Id**
low-timelock-delay
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - minDelay\s*[=:]\s*\d{1,4}[^0-9]
### **Message**
Timelock delay should be at least 1-2 days for major protocols
### **Fix Action**
Set minDelay to 172800 (2 days) or higher
### **Applies To**
  - *.sol

## No proposal threshold

### **Id**
zero-proposal-threshold
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - proposalThreshold.*return\s*0
### **Message**
Anyone can create proposals - consider requiring token stake
### **Fix Action**
Set proposalThreshold to reasonable amount (e.g., 0.1-1% of supply)
### **Applies To**
  - *.sol

## Quorum below 2%

### **Id**
low-quorum
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - quorumNumerator\s*[=:]\s*[01][^0-9]
### **Message**
Quorum below 2% allows minority to pass proposals
### **Fix Action**
Set quorum to at least 4% for security
### **Applies To**
  - *.sol

## Protocol admin is not timelock

### **Id**
admin-not-timelock
### **Severity**
error
### **Type**
regex
### **Pattern**
  - admin\s*=.*(?!timelock|Timelock)
### **Message**
Protocol contracts should be owned by timelock
### **Fix Action**
Transfer ownership to TimelockController address
### **Applies To**
  - *.sol

## Emergency guardian with excessive powers

### **Id**
guardian-too-powerful
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - guardian.*upgrade|guardian.*transfer|emergency.*call\(
### **Message**
Guardian should only have pause capability, not arbitrary execution
### **Fix Action**
Limit guardian to emergencyPause() only
### **Applies To**
  - *.sol

## Voting period too short

### **Id**
voting-period-short
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - votingPeriod.*return\s*\d{1,4}[^0-9]
### **Message**
Voting period under 3 days may not allow adequate participation
### **Fix Action**
Set votingPeriod to at least 5-7 days (36000-50400 blocks)
### **Applies To**
  - *.sol

## No delay before voting starts

### **Id**
no-voting-delay
### **Severity**
info
### **Type**
regex
### **Pattern**
  - votingDelay.*return\s*0
### **Message**
Voting delay allows community to discuss before voting
### **Fix Action**
Set votingDelay to at least 1 day (7200 blocks)
### **Applies To**
  - *.sol

## No auto-delegation for new holders

### **Id**
no-self-delegate
### **Severity**
info
### **Type**
regex
### **Pattern**
  - _afterTokenTransfer(?!.*delegate)
### **Message**
Consider auto-delegating to improve participation
### **Fix Action**
Add auto self-delegation in _afterTokenTransfer
### **Applies To**
  - *.sol