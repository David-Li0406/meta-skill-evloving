# Community Analytics - Sharp Edges

## Vanity Metrics Trap

### **Id**
vanity-metrics-trap
### **Summary**
Optimizing for wrong metrics
### **Severity**
high
### **Situation**
Growing member count while health declines
### **Why**
  Easy metrics are often wrong metrics.
  Leadership asks for simple numbers.
  Growth is visible, health is not.
  
### **Solution**
  ## Avoiding Vanity Metrics
  
  ### Vanity vs Value
  | Vanity | Value |
  |--------|-------|
  | Total members | Active members |
  | Total messages | Conversations |
  | Page views | Time engaged |
  | Followers | Engagement rate |
  
  ### Reporting Balance
  Always pair growth with health:
  - "500 new members, 45% week-1 retention"
  - "10K messages, 3.2 avg thread depth"
  - "20K followers, 5% engagement rate"
  
  ### Executive Dashboard
  - Lead with health, not just growth
  - Show trends, not just snapshots
  - Include qualitative alongside quantitative
  
### **Symptoms**
  - Big numbers, declining engagement
  - Leadership happy, team worried
  - Can't explain business value
### **Detection Pattern**
numbers look good|but engagement|vanity|meaningless

## Data Paralysis

### **Id**
data-paralysis
### **Summary**
Too much data, no decisions
### **Severity**
medium
### **Situation**
Drowning in dashboards but not acting
### **Why**
  Collecting everything possible.
  No clear questions driving analysis.
  Fear of missing something.
  
### **Solution**
  ## From Data to Decision
  
  ### Question-First Analytics
  1. What decision are we making?
  2. What data would inform it?
  3. Collect only that data
  4. Make the decision
  
  ### Metrics Hierarchy
  - North Star: 1 metric (health score)
  - Primary: 3-5 metrics (activity, retention, sentiment)
  - Secondary: 10-15 supporting metrics
  - Diagnostic: As needed for investigation
  
  ### Regular Pruning
  - Quarterly: What metrics did we not use?
  - Delete unused dashboards
  - Simplify reports
  
### **Symptoms**
  - 20+ dashboards
  - Reports nobody reads
  - What should we look at?
  - No action from data
### **Detection Pattern**
too much data|which dashboard|not sure what|overwhelming

## Sentiment Blind

### **Id**
sentiment-blind
### **Summary**
Ignoring qualitative sentiment
### **Severity**
medium
### **Situation**
Metrics look good but members unhappy
### **Why**
  Quantitative is easier to track.
  Sentiment requires interpretation.
  Numbers feel more objective.
  
### **Solution**
  ## Capturing Sentiment
  
  ### Sentiment Sources
  | Source | Frequency | Method |
  |--------|-----------|--------|
  | NPS survey | Quarterly | Scale 1-10 |
  | Pulse checks | Monthly | Quick emoji vote |
  | Exit interviews | On churn | 1:1 or form |
  | Message analysis | Continuous | AI sentiment |
  
  ### Warning Signs
  - Negative tone increasing
  - Complaints in messages
  - Less enthusiasm over time
  - "It's not like it used to be"
  
  ### Integrating Sentiment
  - Include in health score
  - Qualitative in reports
  - Regular member conversations
  
### **Symptoms**
  - Surprise churn
  - Everything seemed fine
  - Negative feedback blindsides
  - Community feels off
### **Detection Pattern**
didn't see it coming|seemed fine|surprised|off vibe