# Disaster Recovery

## Patterns

### **Golden Rules**
  
---
    ##### **Rule**
Define RTO/RPO first
    ##### **Reason**
Drives all architecture decisions
  
---
    ##### **Rule**
Test regularly
    ##### **Reason**
Untested plans fail when needed
  
---
    ##### **Rule**
Automate failover
    ##### **Reason**
Manual steps increase RTO
  
---
    ##### **Rule**
Document runbooks
    ##### **Reason**
Stress impairs memory
  
---
    ##### **Rule**
Include dependencies
    ##### **Reason**
DR is only as strong as weakest link
### **Service Tiers**
  #### **Mission Critical**
    ##### **Rto**
15 minutes
    ##### **Rpo**
1 minute
    ##### **Mtpd**
1 hour
    ##### **Strategy**
active-active
    ##### **Examples**
      - Payment processing
      - Core trading
      - Emergency systems
  #### **Business Critical**
    ##### **Rto**
1 hour
    ##### **Rpo**
15 minutes
    ##### **Mtpd**
4 hours
    ##### **Strategy**
warm-standby
    ##### **Examples**
      - Order management
      - Customer portal
      - CRM
  #### **Business Operational**
    ##### **Rto**
4 hours
    ##### **Rpo**
1 hour
    ##### **Mtpd**
24 hours
    ##### **Strategy**
pilot-light
    ##### **Examples**
      - Reporting
      - Analytics
      - Internal tools
  #### **Business Support**
    ##### **Rto**
24 hours
    ##### **Rpo**
4 hours
    ##### **Mtpd**
3 days
    ##### **Strategy**
backup-restore
    ##### **Examples**
      - Development
      - Testing
      - Archives
### **Dr Strategies**
  #### **Backup Restore**
    ##### **Cost**
$
    ##### **Rto**
Hours
    ##### **Rpo**
Hours
    ##### **Description**
Periodic backups, restore when needed
  #### **Pilot Light**
    ##### **Cost**
$$
    ##### **Rto**
10+ minutes
    ##### **Rpo**
Minutes
    ##### **Description**
Core services running, scale on failover
  #### **Warm Standby**
    ##### **Cost**
$$$
    ##### **Rto**
Minutes
    ##### **Rpo**
Seconds
    ##### **Description**
Scaled-down replica always running
  #### **Active Active**
    ##### **Cost**
$$$$
    ##### **Rto**
Seconds
    ##### **Rpo**
Near-zero
    ##### **Description**
Full redundancy, traffic to both sites
### **Backup Types**
  - full
  - incremental
  - differential
  - snapshot

## Anti-Patterns


---
  #### **Pattern**
Untested plans
  #### **Problem**
Fail during actual disaster
  #### **Solution**
Regular DR drills

---
  #### **Pattern**
Manual failover
  #### **Problem**
Slow RTO, error-prone
  #### **Solution**
Automate failover steps

---
  #### **Pattern**
Ignoring dependencies
  #### **Problem**
Partial recovery
  #### **Solution**
Map all dependencies

---
  #### **Pattern**
Same region backups
  #### **Problem**
Lost with primary
  #### **Solution**
Cross-region replication

---
  #### **Pattern**
Stale runbooks
  #### **Problem**
Wrong procedures
  #### **Solution**
Review after each test

---
  #### **Pattern**
No rollback plan
  #### **Problem**
Stuck in broken state
  #### **Solution**
Always plan failback