# Telegram Mastery - Validations

## No Anti-Spam Bot

### **Id**
no-anti-spam
### **Severity**
high
### **Type**
conceptual
### **Check**
Should have anti-spam protection
### **Indicators**
  - Spam in group
  - No moderation bot
  - Manual spam removal only
### **Message**
No anti-spam bot configured.
### **Fix Action**
Add anti-spam bot (Combot, Rose, or Shieldy) with proper configuration

## No Join Verification

### **Id**
no-captcha
### **Severity**
high
### **Type**
conceptual
### **Check**
Should verify new members
### **Indicators**
  - Bots joining freely
  - Scammers in group
  - No captcha
### **Message**
No captcha or verification for new members.
### **Fix Action**
Enable captcha bot to verify new members are human

## Excessive Admin Permissions

### **Id**
too-many-admins
### **Severity**
medium
### **Type**
conceptual
### **Check**
Admin count should be minimal
### **Indicators**
  - More than 5 human admins
  - Bots with full admin
  - Unknown admins
### **Message**
Too many users with admin permissions.
### **Fix Action**
Audit admins, remove unnecessary ones, minimize bot permissions

## Announcements Mixed with Chat

### **Id**
no-channel-separation
### **Severity**
medium
### **Type**
conceptual
### **Check**
Should separate announcements from discussion
### **Indicators**
  - Important announcements lost in chat
  - No announcement channel
  - Members miss key updates
### **Message**
No separate channel for announcements.
### **Fix Action**
Create announcement channel and link to discussion group

## No Scam Warnings

### **Id**
no-scam-warning
### **Severity**
medium
### **Type**
conceptual
### **Check**
Should warn members about scams
### **Indicators**
  - Members getting scammed
  - No pinned warning
  - No onboarding about scams
### **Message**
No scam warnings for members.
### **Fix Action**
Pin scam warning, educate on 'admins never DM first' rule

## No Slow Mode in Large Group

### **Id**
no-slow-mode
### **Severity**
low
### **Type**
conceptual
### **Check**
Large groups should have slow mode
### **Indicators**
  - Chat moving too fast to follow
  - 10K+ members, no slow mode
  - Spam flooding
### **Message**
Large group without slow mode.
### **Fix Action**
Enable appropriate slow mode based on group size and activity