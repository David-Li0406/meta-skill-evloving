# Discord Mastery - Validations

## No Verification System

### **Id**
no-verification
### **Severity**
high
### **Type**
conceptual
### **Check**
Should have member verification
### **Indicators**
  - Anyone can join and post immediately
  - No captcha or verification
  - Frequent spam/scam issues
### **Message**
No verification system in place.
### **Fix Action**
Set Discord verification level and add verification bot

## Too Many Channels

### **Id**
excessive-channels
### **Severity**
medium
### **Type**
conceptual
### **Check**
Channel count should match server size
### **Indicators**
  - Many empty channels
  - Members confused where to post
  - Activity fragmented
### **Message**
Server has too many channels for its size.
### **Fix Action**
Audit and archive unused channels, consolidate similar ones

## No Automod Configuration

### **Id**
no-automod
### **Severity**
high
### **Type**
conceptual
### **Check**
Should have automated moderation
### **Indicators**
  - Spam gets through
  - Manual mod only
  - Slow response to violations
### **Message**
No automated moderation configured.
### **Fix Action**
Configure automod bot with spam, slur, and scam filters

## Overly Permissive Permissions

### **Id**
weak-permissions
### **Severity**
high
### **Type**
conceptual
### **Check**
Permissions should be minimal
### **Indicators**
  - Too many admins
  - @everyone can mention everyone
  - New members have too many perms
### **Message**
Permissions are too permissive.
### **Fix Action**
Audit permissions, restrict based on principle of least privilege

## No Welcome/Onboarding

### **Id**
no-welcome-flow
### **Severity**
medium
### **Type**
conceptual
### **Check**
Should have structured onboarding
### **Indicators**
  - No welcome message
  - No rules channel
  - No start-here guide
### **Message**
No welcome or onboarding flow.
### **Fix Action**
Create welcome channel, rules, and getting-started guide

## No Moderation Logging

### **Id**
no-mod-logs
### **Severity**
medium
### **Type**
conceptual
### **Check**
Should log moderation actions
### **Indicators**
  - No audit trail
  - Can't review past actions
  - No accountability
### **Message**
Moderation actions not being logged.
### **Fix Action**
Set up mod logging channel with bot integration