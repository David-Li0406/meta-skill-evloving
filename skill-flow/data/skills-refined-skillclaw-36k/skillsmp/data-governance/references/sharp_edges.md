# Data Governance - Sharp Edges

## Data Without Ownership

### **Id**
no-data-owner
### **Severity**
critical
### **Summary**
Critical data has no accountable business owner
### **Symptoms**
  - Data quality issues persist unfixed
  - Nobody approves access requests
  - Conflicting definitions across teams
### **Why**
  Without clear ownership, data quality degrades. When issues arise,
  nobody feels responsible for fixing them. Different teams create
  conflicting definitions leading to inconsistent reporting.
  
### **Gotcha**
  "Who owns the customer data?"
  "IT manages the database."
  "But who defines what 'active customer' means?"
  "... I don't know."
  
  # No business owner = no accountability = bad data!
  
### **Solution**
  1. Assign data owners (business leaders):
     - One owner per data domain
     - Authority to make decisions
     - Accountable for quality
  
  2. Assign data stewards (operational):
     - Day-to-day quality monitoring
     - Maintain metadata
     - Escalate issues to owner
  
  3. Document in data catalog:
     - Owner contact information
     - Steward contact information
     - Escalation path
  

## Outdated Data Catalog

### **Id**
stale-data-catalog
### **Severity**
high
### **Summary**
Catalog doesn't reflect reality so nobody trusts it
### **Symptoms**
  - Tables exist in DB but not catalog
  - Column descriptions outdated
  - Lineage shows old pipelines
### **Why**
  A stale data catalog is worse than no catalog. Users waste time
  checking the catalog only to find wrong information. Eventually
  they stop using it, making the investment worthless.
  
### **Gotcha**
  "The catalog says this table has 10 columns but I see 15."
  "Oh, we added some columns last year."
  "And the description says it's updated daily but..."
  "Yeah, it's hourly now."
  
  # Nobody trusts the catalog anymore!
  
### **Solution**
  1. Automated metadata ingestion:
     - Crawl databases on schedule
     - Detect schema changes
     - Alert on drift
  
  2. CI/CD integration:
     - Update catalog on deploy
     - Block deploys without metadata
     - Version descriptions with code
  
  3. Active metadata:
     - Show actual freshness
     - Real-time lineage from logs
     - Usage metrics from queries
  

## Untracked PII Proliferation

### **Id**
pii-everywhere
### **Severity**
critical
### **Summary**
Personal data copied across systems without tracking
### **Symptoms**
  - Customer emails in analytics warehouse
  - Export files with unmasked data
  - Test environments with production PII
### **Why**
  GDPR and other regulations require knowing where PII lives.
  When data is copied freely, you can't respond to deletion requests,
  can't detect breaches accurately, and face compliance risk.
  
### **Gotcha**
  "We need to delete all John Smith's data per GDPR."
  "It's in the main database, marketing automation, and..."
  "The analytics warehouse, the ML training set, that Excel export
   from last week, the test database..."
  
  # PII is everywhere! Can't delete it all!
  
### **Solution**
  1. PII discovery and classification:
     - Automated scanning for patterns
     - ML-based PII detection
     - Tag PII columns in catalog
  
  2. Data masking:
     - Mask PII for non-prod environments
     - Tokenization for analytics
     - Access controls on sensitive columns
  
  3. Lineage for PII:
     - Track PII data flows
     - Alert on new PII destinations
     - Enable deletion propagation
  

## Quality Checks at Consumption

### **Id**
quality-checked-too-late
### **Severity**
high
### **Summary**
Bad data discovered when reports break
### **Symptoms**
  - Dashboard shows impossible values
  - ML model performance degrades
  - Data issues found by business users
### **Why**
  Checking quality at consumption means bad data has already
  propagated through the system. Fix is expensive - must trace
  back through pipelines and reprocess. Users lose trust.
  
### **Gotcha**
  "Our revenue report shows -$5M for last month."
  "That's impossible - how did this get through?"
  "We only check the final report numbers."
  
  # Bad data flowed through 10 pipelines before anyone noticed!
  
### **Solution**
  1. Shift left - check at source:
     - Validate ingestion data
     - Fail pipelines on quality issues
     - Don't propagate bad data
  
  2. Check at each stage:
     - Quality gates between transforms
     - Anomaly detection on row counts
     - Statistical process control
  
  3. Contract testing:
     - Define expectations per dataset
     - Automated quality tests in CI
     - Quarantine failing data
  