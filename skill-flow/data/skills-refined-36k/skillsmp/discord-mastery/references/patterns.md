# Discord Mastery

## Patterns


---
  #### **Name**
Server Architecture
  #### **Description**
Designing organized, scalable server structure
  #### **When To Use**
When setting up or restructuring a Discord server
  #### **Implementation**
    ## Discord Server Architecture
    
    ### Category Structure
    ```
    WELCOME
    ├── #rules
    ├── #introductions
    ├── #start-here
    └── #announcements
    
    COMMUNITY
    ├── #general
    ├── #off-topic
    ├── #wins
    └── #help
    
    TOPIC SPECIFIC (varies)
    ├── #topic-1
    ├── #topic-2
    └── #topic-3
    
    RESOURCES
    ├── #resources
    ├── #links
    └── #faq
    
    VOICE
    ├── General VC
    ├── Focus Room
    └── Events Stage
    
    MOD ONLY
    ├── #mod-chat
    ├── #mod-logs
    └── #escalations
    ```
    
    ### Channel Count Guidelines
    | Server Size | Max Channels | Categories |
    |-------------|--------------|------------|
    | < 500 | 10-15 | 3-4 |
    | 500-2K | 15-25 | 4-6 |
    | 2K-10K | 25-40 | 6-8 |
    | 10K+ | 40-60 | 8-12 |
    
    ### Common Mistakes
    - Too many channels (cognitive overload)
    - No clear purpose per channel
    - Buried important channels
    - Inconsistent naming
    

---
  #### **Name**
Role System Design
  #### **Description**
Permission-based role hierarchy
  #### **When To Use**
When designing access control
  #### **Implementation**
    ## Role Hierarchy
    
    ### Standard Roles (Top to Bottom)
    ```
    ADMIN (Full perms)
    ├── Lead Moderator
    ├── Senior Moderator
    ├── Moderator
    ├── Trial Moderator
    ├── VIP/OG
    ├── Active Member
    ├── Verified
    └── New Member
    ```
    
    ### Role Assignment
    | Role | How Earned | Perks |
    |------|------------|-------|
    | Verified | Complete onboarding | Basic access |
    | Active | Time + activity | More channels |
    | VIP | Contribution | Special access |
    | Mod | Application/invite | Mod tools |
    
    ### Permission Best Practices
    - Start restrictive, grant permissions up
    - Use role hierarchy properly
    - Avoid @everyone permissions
    - Regular permission audits
    

---
  #### **Name**
Bot Ecosystem
  #### **Description**
Strategic bot deployment
  #### **When To Use**
When setting up or optimizing bots
  #### **Implementation**
    ## Bot Strategy
    
    ### Essential Bots
    | Purpose | Options | Notes |
    |---------|---------|-------|
    | Moderation | Carl-bot, Wick, Dyno | Pick one main |
    | Welcome/Roles | Carl-bot, MEE6 | Reaction roles |
    | Leveling | MEE6, Tatsu, Arcane | Optional |
    | Tickets | Ticket Tool, Carl-bot | For support |
    | Custom | Custom bot | For unique needs |
    
    ### Configuration Principles
    - One primary moderation bot
    - Avoid duplicate functionality
    - Test before deploying
    - Document all bot settings
    - Regular bot audits
    
    ### Automod Setup
    | Rule | Action | Notes |
    |------|--------|-------|
    | Spam | Delete + warn | Link cooldown |
    | Slurs | Delete + timeout | Use blocklist |
    | Raids | Lockdown | Mention spam |
    | Scams | Delete + ban | Crypto scams |
    

## Anti-Patterns


---
  #### **Name**
Channel Sprawl
  #### **Description**
Too many channels killing activity
  #### **Why Bad**
    Activity diluted across channels.
    Members don't know where to post.
    Dead channels look bad.
    
  #### **What To Do Instead**
    Start minimal, add only when needed.
    Archive unused channels.
    Use threads for sub-topics.
    Quality over quantity.
    

---
  #### **Name**
Bot Overload
  #### **Description**
Too many bots cluttering server
  #### **Why Bad**
    Confusing for members.
    Overlapping functionality.
    Bot spam in channels.
    Maintenance nightmare.
    
  #### **What To Do Instead**
    Audit bots quarterly.
    One bot per function.
    Remove unused bots.
    Document configurations.
    

---
  #### **Name**
Over-Gamification
  #### **Description**
Excessive XP/leveling focus
  #### **Why Bad**
    Members game the system.
    Quantity over quality.
    XP farming behavior.
    Loses meaning.
    
  #### **What To Do Instead**
    Subtle gamification.
    Meaningful levels (access, not just status).
    Quality-based, not just activity.
    