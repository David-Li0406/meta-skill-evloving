# Community Tooling

## Patterns


---
  #### **Name**
Community Tool Stack
  #### **Description**
Building a cohesive community tech stack
  #### **When To Use**
When setting up or evaluating community tools
  #### **Implementation**
    ## Community Tool Stack Framework
    
    ### Core Stack Layers
    | Layer | Purpose | Examples |
    |-------|---------|----------|
    | Platform | Where community lives | Discord, Slack, Circle |
    | Moderation | Keep community safe | Wick, MEE6, Carl-bot |
    | Analytics | Measure community | Orbit, Common Room |
    | CRM | Track relationships | Orbit, Notion, Airtable |
    | Automation | Streamline workflows | Zapier, n8n, custom |
    
    ### Stack by Community Size
    | Size | Stack Complexity |
    |------|------------------|
    | <100 | Platform + basic mod |
    | 100-1K | + Analytics + Zapier |
    | 1K-10K | + CRM + advanced mods |
    | 10K+ | Full stack + custom tools |
    
    ### Integration Philosophy
    - Data should flow between tools
    - Single source of truth
    - Avoid duplicate data entry
    - Central member database
    
    ### Tool Selection Criteria
    | Factor | Weight |
    |--------|--------|
    | Solves real problem | Critical |
    | Integration capability | High |
    | Team can use it | High |
    | Cost appropriate | Medium |
    | Scalability | Medium |
    

---
  #### **Name**
Discord Bot Stack
  #### **Description**
Recommended Discord bot configurations
  #### **When To Use**
When setting up Discord bots
  #### **Implementation**
    ## Discord Bot Stack
    
    ### Essential Bots
    | Bot | Purpose | When to Add |
    |-----|---------|-------------|
    | Carl-bot | Roles, welcome, logging | Day 1 |
    | MEE6 | Levels, moderation | Day 1 |
    | Wick | Anti-raid, security | Day 1 for Web3 |
    | Collab.Land | Token gating | Web3 communities |
    
    ### Specialized Bots
    | Bot | Purpose |
    |-----|---------|
    | Ticket Tool | Support tickets |
    | Statbot | Server analytics |
    | Dyno | Moderation, custom commands |
    | Zira | Reaction roles |
    | Suggester | Feature requests |
    
    ### Bot Best Practices
    - Don't add bots "just in case"
    - Test in staging server first
    - Document configuration
    - Regular permission audit
    - Have backup alternatives
    
    ### Custom Bots
    - Consider when: Unique needs, branding, data ownership
    - Build vs buy decision matrix
    - Maintenance overhead
    - Security considerations
    

---
  #### **Name**
Community Platform Comparison
  #### **Description**
Evaluating community platforms
  #### **When To Use**
When choosing or switching platforms
  #### **Implementation**
    ## Community Platform Comparison
    
    ### Platform Matrix
    | Platform | Best For | Limitations |
    |----------|----------|-------------|
    | Discord | Gaming, Web3, dev | Discovery, SEO |
    | Slack | Professional, paid | Cost at scale |
    | Circle | Courses, membership | Less real-time |
    | Discourse | Long-form, support | Less chat-like |
    | Mighty Networks | Creators, courses | Limited integrations |
    
    ### Decision Criteria
    - Where is your audience already?
    - Real-time vs async needs
    - Content discoverability
    - Monetization needs
    - Scale expectations
    
    ### Migration Considerations
    - Can you export member data?
    - How to move active discussions?
    - Communication plan
    - Transition period
    - What gets left behind
    

---
  #### **Name**
Community Analytics Stack
  #### **Description**
Tools for measuring community health
  #### **When To Use**
When setting up community measurement
  #### **Implementation**
    ## Community Analytics Stack
    
    ### Analytics Platforms
    | Platform | Strength | Best For |
    |----------|----------|----------|
    | Orbit | Developer communities | OSS, DevRel |
    | Common Room | Multi-platform | Enterprise |
    | Commsor | Team attribution | Sales-driven |
    | Statbot | Discord-specific | Discord focus |
    
    ### DIY Analytics
    - Notion/Airtable for manual tracking
    - Platform native analytics
    - Spreadsheet dashboards
    - Custom bot logging
    
    ### What to Track
    | Metric | Tool Source |
    |--------|-------------|
    | Active members | Platform + Orbit |
    | Engagement | Statbot + Platform |
    | Growth | Platform + analytics |
    | Support volume | Ticket tool |
    | Sentiment | Manual + keywords |
    
    ### Data Integration
    - Connect platforms to analytics
    - Unified member view
    - Activity across channels
    - Export capabilities
    

## Anti-Patterns


---
  #### **Name**
Tool Sprawl
  #### **Description**
Too many tools, no coherent stack
  #### **Why Bad**
    Data fragmented.
    Team overwhelmed.
    Nothing integrated.
    Expensive and confusing.
    
  #### **What To Do Instead**
    Start with essentials.
    Add tools only for real problems.
    Prioritize integration.
    Regular stack audit.
    

---
  #### **Name**
Bot Overload
  #### **Description**
Too many bots in Discord
  #### **Why Bad**
    Confusing for members.
    Conflicting commands.
    Performance issues.
    Security risks.
    
  #### **What To Do Instead**
    Maximum 5-7 bots.
    Clear purpose for each.
    Remove unused bots.
    Consolidate functionality.
    

---
  #### **Name**
Tool Before Process
  #### **Description**
Buying tool before defining workflow
  #### **Why Bad**
    Tool doesn't fit process.
    Forces bad workflows.
    Wasted money and time.
    
  #### **What To Do Instead**
    Define process first.
    Manual before automatic.
    Tool to enhance, not define.
    Trial before commit.
    