# Education Platforms

## Patterns


---
  #### **Name**
Platform Selection Framework
  #### **Description**
Choosing the right course platform
  #### **When To Use**
When selecting a course platform
  #### **Implementation**
    ## Platform Selection Framework
    
    ### Decision Matrix
    | Factor | Weight | Questions |
    |--------|--------|-----------|
    | Core features | High | Does it do what I need? |
    | Pricing model | High | Can I afford it at scale? |
    | Ease of use | Medium | Can I manage it myself? |
    | Customization | Medium | Can I brand it properly? |
    | Integrations | Medium | Does it connect to my tools? |
    | Support | Low | Can I get help when stuck? |
    
    ### Platform Categories
    | Type | Examples | Best For |
    |------|----------|----------|
    | All-in-one | Kajabi, Kartra | Solo educators, bundled needs |
    | Course-focused | Teachable, Thinkific | Course-first business |
    | Community-first | Circle, Mighty Networks | Community + courses |
    | Enterprise | Docebo, Cornerstone | Large orgs, compliance |
    | Open source | Moodle, Open edX | Full control, tech team |
    
    ### Quick Recommendation
    | Situation | Platform |
    |-----------|----------|
    | First course, simple | Teachable or Thinkific |
    | Courses + community | Circle or Mighty Networks |
    | All-in-one marketing | Kajabi |
    | Full customization | Custom (Next.js + headless) |
    | Enterprise/compliance | Docebo or Cornerstone |
    

---
  #### **Name**
Platform Comparison Matrix
  #### **Description**
Detailed comparison of major platforms
  #### **When To Use**
When evaluating specific platforms
  #### **Implementation**
    ## Platform Comparison Matrix
    
    ### Course Platforms (2024)
    | Platform | Price | Best For | Weakness |
    |----------|-------|----------|----------|
    | Teachable | $59-249/mo | Beginners, simplicity | Limited community |
    | Thinkific | $49-199/mo | Course + membership | Basic marketing |
    | Kajabi | $149-399/mo | All-in-one | Expensive, opinionated |
    | Podia | $39-199/mo | Digital products | Limited features |
    | LearnDash | $199/yr | WordPress users | Needs WordPress |
    
    ### Community + Courses
    | Platform | Price | Best For | Weakness |
    |----------|-------|----------|----------|
    | Circle | $49-219/mo | Community-first | Courses less mature |
    | Mighty Networks | $99-315/mo | Courses + community | Can be slow |
    | Skool | $99/mo | Gamified community | Limited course features |
    
    ### Feature Comparison
    | Feature | Teachable | Kajabi | Thinkific | Circle |
    |---------|-----------|--------|-----------|--------|
    | Course hosting | ✅ | ✅ | ✅ | ✅ |
    | Community | ❌ | Basic | Basic | ✅ |
    | Email marketing | Basic | ✅ | Basic | ❌ |
    | Landing pages | Basic | ✅ | Basic | ❌ |
    | Cohort features | ❌ | ❌ | ✅ | ✅ |
    | API access | ✅ | Limited | ✅ | ✅ |
    
    ### Hidden Costs to Consider
    - Transaction fees (some platforms take %)
    - Additional user charges
    - Storage limits
    - Integration costs
    - Migration costs later
    

---
  #### **Name**
Build vs Buy Decision
  #### **Description**
When to build custom vs use SaaS
  #### **When To Use**
When considering custom development
  #### **Implementation**
    ## Build vs Buy Decision
    
    ### When to Buy (SaaS Platform)
    - First course
    - No development team
    - Need to launch fast
    - Standard course format
    - Budget under $5K/month
    
    ### When to Build Custom
    - Unique learning format
    - Tight integration needs
    - 10K+ students
    - Platform taking too much revenue
    - Long-term cost optimization
    
    ### Hybrid Approach
    | Component | Buy | Build |
    |-----------|-----|-------|
    | Video hosting | Vimeo, Bunny | |
    | Payments | Stripe | |
    | Auth | | Custom or Clerk |
    | Course UI | | Custom |
    | Community | Discord, Circle | |
    
    ### Custom Stack Options
    | Stack | Complexity | Flexibility |
    |-------|------------|-------------|
    | WordPress + LearnDash | Low | Medium |
    | Next.js + Headless CMS | High | High |
    | Rails + Custom | High | High |
    | No-code (Bubble) | Medium | Medium |
    
    ### Total Cost Comparison (5 year)
    | Approach | Year 1 | Year 5 Total |
    |----------|--------|--------------|
    | Teachable Pro | $3K | $15K |
    | Kajabi Growth | $5K | $25K |
    | Custom build | $30-50K | $50-70K |
    

---
  #### **Name**
Platform Migration
  #### **Description**
Moving between course platforms
  #### **When To Use**
When switching platforms
  #### **Implementation**
    ## Platform Migration
    
    ### Migration Checklist
    - [ ] Export student data
    - [ ] Export course content
    - [ ] Document current structure
    - [ ] Test new platform thoroughly
    - [ ] Plan communication
    - [ ] Set redirect strategy
    - [ ] Pick low-activity time
    
    ### What Migrates Easily
    - Video files (re-upload or link)
    - Text content
    - Student email list
    - Basic course structure
    
    ### What Doesn't Migrate
    - Progress data (usually lost)
    - Platform-specific features
    - URLs and bookmarks
    - Platform integrations
    - Quiz results
    
    ### Migration Timeline
    | Phase | Duration |
    |-------|----------|
    | Planning | 2 weeks |
    | Content export/import | 2-4 weeks |
    | Testing | 1-2 weeks |
    | Parallel run | 1-2 weeks |
    | Switch + communication | 1 week |
    
    ### Communication Template
    ```
    Subject: We're moving to a better home
    
    Good news: We've upgraded to a new platform that will
    give you [specific benefits].
    
    What you need to do:
    1. Your login is the same
    2. New URL: [link]
    3. Progress resets (we're giving you [bonus])
    
    Questions? Reply to this email.
    ```
    

## Anti-Patterns


---
  #### **Name**
Feature Chasing
  #### **Description**
Choosing platform for features you won't use
  #### **Why Bad**
    Paying for unused features.
    More complex than needed.
    Harder to switch later.
    
  #### **What To Do Instead**
    List features you NEED now.
    Ignore the rest.
    Choose simplest option that works.
    Upgrade later if needed.
    

---
  #### **Name**
Price-First Decision
  #### **Description**
Choosing cheapest option
  #### **Why Bad**
    Hidden costs emerge.
    Missing critical features.
    Limits growth.
    Migrating costs more than premium would have.
    
  #### **What To Do Instead**
    Calculate true cost at scale.
    Include transaction fees.
    Include opportunity cost.
    Think 2-3 years ahead.
    

---
  #### **Name**
Premature Custom Build
  #### **Description**
Building custom before validating
  #### **Why Bad**
    Months of development.
    Not sure course will sell.
    Technical debt before revenue.
    Could use that time to teach.
    
  #### **What To Do Instead**
    Use SaaS for v1.
    Validate demand.
    Build custom only if platform is limiting.
    Treat custom as v2 or v3.
    