# Telegram Mastery - Sharp Edges

## Telegram Scam Dm

### **Id**
telegram-scam-dm
### **Summary**
Scammers DMing members pretending to be admins
### **Severity**
high
### **Situation**
Members getting scammed via fake admin DMs
### **Why**
  Anyone can DM anyone on Telegram.
  Easy to impersonate admin name/photo.
  New members don't know real admins.
  
### **Solution**
  ## Preventing Admin Impersonation
  
  ### Education
  - Pin warning: "Admins NEVER DM first"
  - Regular reminders in chat
  - Onboarding includes scam warning
  - List real admin usernames
  
  ### Technical Measures
  - Admins use unique, hard-to-copy usernames
  - Link to official admin list
  - Report impersonators to Telegram
  - Ban and warn about known scam accounts
  
  ### Response to Reports
  1. Take screenshot of scam DM
  2. Report to Telegram
  3. Ban scammer from group
  4. Alert community
  5. Support scammed member
  
### **Symptoms**
  - Admin DMed me asking for...
  - Members losing funds
  - Fake admin accounts
  - Phishing links in DMs
### **Detection Pattern**
admin dm|fake admin|scam|impersonat

## Telegram Bot Takeover

### **Id**
telegram-bot-takeover
### **Summary**
Bot with admin rights gets compromised
### **Severity**
high
### **Situation**
Malicious bot or compromised bot wreaks havoc
### **Why**
  Bot given full admin rights.
  Bot token leaked or service compromised.
  No backup admin access.
  
### **Solution**
  ## Bot Security
  
  ### Permission Principle
  - Only grant permissions bot needs
  - Never give "Add Admins" to bots
  - Avoid "Delete Messages" unless needed
  - Review bot permissions quarterly
  
  ### Essential Permissions Only
  | Bot Type | Needs |
  |----------|-------|
  | Anti-spam | Delete messages, ban users |
  | Welcome | Post messages |
  | Analytics | Read messages only |
  
  ### Recovery Plan
  - Multiple human admins (not just bot)
  - Know how to remove bot quickly
  - Backup admin on standby
  - Regular permission audits
  
### **Symptoms**
  - Bot misbehaving
  - Unexpected bans
  - Spam from bot
  - Group settings changed
### **Detection Pattern**
bot problem|compromised|hacked|malicious

## Telegram Slow Mode Wars

### **Id**
telegram-slow-mode-wars
### **Summary**
Slow mode too aggressive or too lenient
### **Severity**
medium
### **Situation**
Chat either too slow or too spammy
### **Why**
  One-size-fits-all approach.
  Not adjusting to activity.
  Member complaints ignored.
  
### **Solution**
  ## Slow Mode Strategy
  
  ### Guidelines
  | Group Size | Activity | Slow Mode |
  |------------|----------|-----------|
  | < 1K | Low | None |
  | < 1K | High | 30s |
  | 1K-10K | Normal | 30s-1min |
  | 1K-10K | Busy | 1-5min |
  | 10K+ | Normal | 1-5min |
  | Any | During raid | Max |
  
  ### Dynamic Adjustment
  - Increase during high activity
  - Decrease during quiet times
  - Temporary increase for events
  - Communicate changes
  
  ### Alternatives to Slow Mode
  - Topic threads (separates conversations)
  - Dedicated Q&A times
  - Announcement channel (low volume)
  
### **Symptoms**
  - Why can't I send messages?
  - Chat moving too fast
  - Important messages lost
  - Member frustration
### **Detection Pattern**
slow mode|can't send|too fast|too slow

## Telegram Privacy Leak

### **Id**
telegram-privacy-leak
### **Summary**
Member phone numbers or info exposed
### **Severity**
high
### **Situation**
Privacy settings expose member information
### **Why**
  Default Telegram settings show phone to contacts.
  Admins can see joiner phone numbers.
  Members unaware of privacy settings.
  
### **Solution**
  ## Privacy Protection
  
  ### Educate Members
  Settings → Privacy → Phone Number → Nobody
  Settings → Privacy → Forwarded Messages → Nobody
  Settings → Privacy → Profile Photo → Contacts/Nobody
  
  ### Admin Responsibility
  - Never share/screenshot member phone numbers
  - Use usernames for all communication
  - Clear policy on data handling
  - Minimal data collection
  
  ### Group Settings
  - Disable "Save Content" if sensitive
  - Consider invite links over adding
  - Regular member list hygiene
  
### **Symptoms**
  - Members doxxed
  - Phone numbers leaked
  - Privacy complaints
  - Legal concerns
### **Detection Pattern**
phone number|privacy|doxx|data leak