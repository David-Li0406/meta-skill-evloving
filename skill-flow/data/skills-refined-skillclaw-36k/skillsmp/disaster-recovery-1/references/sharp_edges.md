# Disaster Recovery - Sharp Edges

## Disaster Recovery Plan Never Tested

### **Id**
untested-dr-plan
### **Severity**
critical
### **Summary**
DR plan exists on paper but has never been executed
### **Symptoms**
  - Last DR test was years ago
  - Team doesn't know the runbook
  - Backup restore times are unknown
### **Why**
  An untested DR plan is not a plan - it's hopeful documentation.
  Real disasters reveal gaps: missing passwords, changed infrastructure,
  broken automation, and team members who don't know their roles.
  
### **Gotcha**
  "Our DR plan says we can recover in 4 hours"
  "When did you last test it?"
  "We... haven't. But it's documented!"
  
  # The disaster happens. Recovery takes 3 days.
  
### **Solution**
  1. Schedule regular DR drills:
     - Quarterly for critical systems
     - Annual full-scale exercises
     - Document and review results
  
  2. Game day exercises:
     - Simulate real scenarios
     - Include on-call team
     - Practice communication
  
  3. Automated testing:
     - Restore backups weekly
     - Verify data integrity
     - Measure actual RTO
  

## Backups in Same Region as Primary

### **Id**
single-region-backups
### **Severity**
critical
### **Summary**
All backups stored in the same region as production data
### **Symptoms**
  - Fast backup/restore times
  - Low storage costs
  - No cross-region replication
### **Why**
  Regional disasters (data center fire, natural disaster, provider outage)
  can take out both your primary data AND your backups. Cross-region
  replication is essential for true disaster recovery.
  
### **Gotcha**
  "Where are our backups stored?"
  "us-east-1, same as production for fast restores"
  "And if us-east-1 goes down?"
  "..."
  
  # AWS us-east-1 outage takes down both primary and backups
  
### **Solution**
  1. Cross-region backup replication:
     - Replicate to at least one other region
     - Consider different cloud provider
     - Verify replication is working
  
  2. Backup verification:
     - Test restores from DR region
     - Verify data integrity
     - Document restore procedures
  
  3. Consider 3-2-1 rule:
     - 3 copies of data
     - 2 different storage types
     - 1 offsite location
  

## Manual Steps in Failover Process

### **Id**
manual-failover-steps
### **Severity**
high
### **Summary**
Failover requires manual intervention that slows recovery
### **Symptoms**
  - Failover requires SSH access
  - Manual DNS changes needed
  - Database promotion is manual
### **Why**
  During a disaster, stress is high and people make mistakes.
  Manual steps add time to RTO and introduce human error.
  What takes 5 minutes in practice takes 30 under pressure.
  
### **Gotcha**
  "Step 5: SSH to the replica and run promote_to_primary.sh"
  "I can't find the SSH key!"
  "It's in the password vault"
  "Which password vault?"
  
  # 45 minutes lost finding credentials
  
### **Solution**
  1. Automate everything:
     - Scripted failover procedures
     - Automated health checks
     - Automatic DNS updates
  
  2. One-click failover:
     - Single command to initiate
     - All steps automated
     - Rollback capability
  
  3. Eliminate dependencies:
     - No SSH required
     - No manual approvals during DR
     - Pre-authorized actions
  

## Dependencies Not Mapped for DR

### **Id**
missing-dependency-map
### **Severity**
high
### **Summary**
DR plan doesn't account for all system dependencies
### **Symptoms**
  - Service starts but can't function
  - Missing third-party services
  - Authentication fails after failover
### **Why**
  Modern systems have many dependencies: databases, caches, queues,
  third-party APIs, DNS, authentication providers. If your DR plan
  doesn't account for all of them, recovery is incomplete.
  
### **Gotcha**
  "We failed over the application successfully!"
  "Great, is it working?"
  "No, it can't connect to Redis"
  "Did we fail over Redis?"
  "...that wasn't in the plan"
  
  # Application is up but non-functional
  
### **Solution**
  1. Complete dependency mapping:
     - Internal services
     - Databases and caches
     - Third-party APIs
     - Authentication/SSO
     - DNS and CDN
  
  2. Tiered recovery plan:
     - Infrastructure first
     - Data stores second
     - Applications third
     - Verification last
  
  3. Regular dependency audits:
     - Review when adding services
     - Update DR plan accordingly
     - Test full-stack recovery
  

## No Chaos Engineering Practice

### **Id**
no-chaos-engineering
### **Severity**
medium
### **Summary**
System resilience is assumed but never tested
### **Symptoms**
  - Single points of failure unknown
  - Failure modes untested
  - Team lacks incident experience
### **Why**
  You can't know how your system fails until you make it fail.
  Chaos engineering in production reveals weaknesses before
  real disasters do. Teams that practice handling failures
  respond better during real incidents.
  
### **Gotcha**
  "Our system is highly available"
  "What happens if the database fails?"
  "It should fail over automatically"
  "Have you tested it?"
  "No, but we designed it that way"
  
  # Theory doesn't survive contact with reality
  
### **Solution**
  1. Start small:
     - Kill single instances
     - Add network latency
     - Fill disk space
  
  2. Game days:
     - Planned chaos experiments
     - Team observes and learns
     - Document discoveries
  
  3. Continuous chaos:
     - Chaos Monkey in production
     - Random failure injection
     - Build resilience into culture
  