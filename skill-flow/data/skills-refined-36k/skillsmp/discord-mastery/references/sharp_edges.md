# Discord Mastery - Sharp Edges

## Server Raids

### **Id**
server-raids
### **Summary**
Coordinated attack on server
### **Severity**
high
### **Situation**
Multiple accounts joining and spamming/causing chaos
### **Why**
  Server linked publicly.
  No verification gate.
  Slow mod response.
  
### **Solution**
  ## Raid Prevention & Response
  
  ### Prevention
  - Enable verification level (Medium+)
  - Use verification bot/captcha
  - Limit new member permissions
  - Hide sensitive channels from new members
  
  ### Detection
  - Unusual join spike
  - New accounts posting immediately
  - Same/similar messages
  - Mention spam
  
  ### Response Protocol
  1. IMMEDIATE: Enable slowmode (all channels)
  2. IF SEVERE: Lock server (disable join)
  3. Ban raid accounts
  4. Review logs for patterns
  5. Report to Discord Trust & Safety
  
  ### Automod Settings for Raids
  ```
  - Block mass mentions (5+ in message)
  - Block new account spam (< 1 day old)
  - Enable anti-raid mode in modbot
  ```
  
### **Symptoms**
  - Spam flood
  - Mass joins
  - Chaos in channels
  - Members panicking
### **Detection Pattern**
raid|spam|mass join|attack|flooded

## Permission Creep

### **Id**
permission-creep
### **Summary**
Permissions granted carelessly over time
### **Severity**
medium
### **Situation**
Too many people with too many permissions
### **Why**
  Giving perms to fix quick issues.
  Not revoking when roles change.
  No regular audits.
  
### **Solution**
  ## Permission Hygiene
  
  ### Audit Checklist
  - [ ] Who has admin? (Should be 2-3 max)
  - [ ] Who can ban? (Mods only)
  - [ ] Who can manage channels? (Leads only)
  - [ ] Who can @everyone? (Admins only)
  
  ### Cleanup Process
  1. Export current role/perm list
  2. Review each elevated role
  3. Remove unnecessary permissions
  4. Document who has what and why
  
  ### Prevention
  - Grant minimum necessary
  - Document permission grants
  - Quarterly permission audits
  - Revoke on role change
  
### **Symptoms**
  - Who gave them perms?
  - Accidental @everyone
  - Unauthorized changes
  - Security concerns
### **Detection Pattern**
who has|too many|permission|security

## Dead Channel Syndrome

### **Id**
dead-channel-syndrome
### **Summary**
Many channels with no activity
### **Severity**
medium
### **Situation**
Server looks abandoned with empty channels
### **Why**
  Created too many channels upfront.
  Topics that didn't pan out.
  No archive strategy.
  
### **Solution**
  ## Channel Health
  
  ### Activity Audit
  | Last Message | Action |
  |--------------|--------|
  | < 7 days | Healthy |
  | 7-30 days | Monitor |
  | 30-90 days | Consider archiving |
  | > 90 days | Archive or delete |
  
  ### Archive Process
  1. Create "Archive" category (hidden from most)
  2. Move dead channels there
  3. Or export and delete
  4. Announce consolidation
  
  ### Prevention
  - Start with fewer channels
  - Earn channels through demand
  - Use threads for temp topics
  - Regular channel reviews
  
### **Symptoms**
  - Empty channels
  - Where is everyone?
  - Activity in 2-3 channels only
  - New members confused
### **Detection Pattern**
dead|empty|no one uses|too many channels

## Verification Bypass

### **Id**
verification-bypass
### **Summary**
Scammers getting through verification
### **Severity**
high
### **Situation**
Bad actors passing verification and scamming members
### **Why**
  Verification too simple.
  No ongoing monitoring.
  Scam patterns evolve.
  
### **Solution**
  ## Anti-Scam Measures
  
  ### Verification Layers
  1. Discord's built-in level (phone/email)
  2. Bot captcha (Wick, Captcha.bot)
  3. Manual review for suspicious
  4. Probation period for new members
  
  ### Scam Detection
  | Pattern | Action |
  |---------|--------|
  | DM about crypto | Warn members, ban scammer |
  | "Admin" impersonation | Immediate ban |
  | Fake giveaway links | Delete, ban, report |
  | NFT mint links from new accounts | Delete, ban |
  
  ### Member Education
  - Pin scam warnings
  - Regular reminders
  - Reporting mechanism
  - Staff never DM first policy
  
### **Symptoms**
  - Members getting scammed
  - Fake admin DMs
  - Crypto/NFT scam messages
  - Phishing links
### **Detection Pattern**
scam|hack|fake admin|stolen|phishing