# Telegram Mastery

## Patterns


---
  #### **Name**
Group vs Channel Strategy
  #### **Description**
When to use groups vs channels
  #### **When To Use**
When designing Telegram presence
  #### **Implementation**
    ## Groups vs Channels
    
    ### Telegram Channels
    - One-way broadcast
    - Unlimited subscribers
    - No member list visible
    - Best for: Announcements, content
    
    ### Telegram Groups
    - Two-way conversation
    - Up to 200K members
    - Member interaction
    - Best for: Community, support
    
    ### Recommended Setup
    ```
    MAIN CHANNEL (announcements)
    ├── Linked Discussion Group
    └── (Optional) Comments enabled
    
    COMMUNITY GROUP (conversation)
    ├── Main chat
    └── (Optional) Topic threads
    
    SUPPORT GROUP (help)
    └── Separate from main chat
    ```
    
    ### When to Split
    | Situation | Action |
    |-----------|--------|
    | > 5K members, noisy | Consider topic threads |
    | Different languages | Language-specific groups |
    | Different purposes | Separate groups |
    | Too many support Qs | Dedicated support group |
    

---
  #### **Name**
Bot Automation
  #### **Description**
Essential bot setup for Telegram
  #### **When To Use**
When setting up group automation
  #### **Implementation**
    ## Telegram Bot Stack
    
    ### Essential Bots
    | Purpose | Bot | Setup |
    |---------|-----|-------|
    | Anti-spam | Combot, Rose, Group Help | Add as admin |
    | Welcome | Rose, Shieldy | Configure messages |
    | Captcha | Shieldy, Captcha Bot | Verify humans |
    | Moderation | Combot, Rose | Ban/warn system |
    | Analytics | Combot, TGStat | Track metrics |
    
    ### Anti-Spam Configuration
    ```
    Must-have rules:
    - No forwarded messages from non-members
    - No links from new members (first 24h)
    - Captcha on join
    - Ban crypto scam patterns
    - Rate limit messages
    ```
    
    ### Moderation Commands
    | Command | Action |
    |---------|--------|
    | /ban | Ban user |
    | /warn | Issue warning |
    | /mute | Mute user |
    | /kick | Remove without ban |
    | /report | Report to mods |
    

---
  #### **Name**
Large Group Management
  #### **Description**
Managing groups with 10K+ members
  #### **When To Use**
When scaling Telegram groups
  #### **Implementation**
    ## Scaling Telegram Groups
    
    ### Challenges at Scale
    - Message flood (hundreds/hour)
    - Spam and scam attempts
    - Signal vs noise
    - Moderation coverage
    
    ### Solutions
    | Problem | Solution |
    |---------|----------|
    | Too fast | Slow mode (30s-5min) |
    | Spam | Aggressive automod |
    | Noise | Topic threads |
    | Coverage | Global mod team |
    
    ### Topic Threads (New Feature)
    - Organize conversations by topic
    - Members choose their topics
    - Reduces main chat noise
    - Works for 10K+ groups
    
    ### Moderation at Scale
    - 1 mod per 2-5K members
    - 24/7 coverage across timezones
    - Clear escalation path
    - Bot handles 90% of spam
    

## Anti-Patterns


---
  #### **Name**
No Captcha = Spam Hell
  #### **Description**
Running open group without verification
  #### **Why Bad**
    Bots flood the group.
    Scammers DM members.
    Real members leave.
    
  #### **What To Do Instead**
    Mandatory captcha on join.
    New member restrictions.
    Anti-spam bot from day one.
    

---
  #### **Name**
Admin Permission Sprawl
  #### **Description**
Too many people with admin rights
  #### **Why Bad**
    Security risk.
    Inconsistent moderation.
    Accidental damage.
    
  #### **What To Do Instead**
    Minimal admins (2-3).
    Use mod bots with limited perms.
    Regular admin audit.
    

---
  #### **Name**
Mixing Announcements and Chat
  #### **Description**
Using same group for announcements and discussion
  #### **Why Bad**
    Important announcements lost in chat.
    Can't have read-only announcements.
    Members miss key info.
    
  #### **What To Do Instead**
    Separate channel for announcements.
    Link channel to discussion group.
    Pin important messages.
    