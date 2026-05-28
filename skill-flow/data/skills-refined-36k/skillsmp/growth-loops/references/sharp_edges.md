# Growth Loops - Sharp Edges

## Vanity Loop Metrics

### **Id**
vanity-loop-metrics
### **Summary**
Measuring the wrong loop metrics
### **Severity**
high
### **Situation**
Loop appears healthy but growth doesn't follow
### **Why**
  Tracking shares instead of conversions.
  Counting invites sent, not accepted.
  Ignoring quality of loop-acquired users.
  
### **Solution**
  ## Correct Loop Metrics
  
  ### What NOT to Measure (Vanity)
  - Invites sent (not accepted)
  - Shares clicked (not converted)
  - Content created (not discovered)
  - Referral links generated (not used)
  
  ### What TO Measure (Actionable)
  
  **Viral Loop**
  - Invites sent per user (who reach invite point)
  - Invite acceptance rate
  - Accepted invite → Signup rate
  - Referred user 30-day retention
  - Referred user LTV vs organic LTV
  
  **Content Loop**
  - Content indexed / Content created
  - Impressions per piece of content
  - Click-through rate from search/social
  - Visitor → Creator conversion
  - Creator 30-day content velocity
  
  **Paid Loop**
  - CAC by cohort (not blended)
  - Payback period (actual, not projected)
  - LTV of paid-acquired vs organic
  - Contribution margin after CAC
  
  ### Dashboard Structure
  ```
  Loop Health Score = (
    Conversion efficiency ×
    Cycle speed ×
    Output quality
  )
  ```
  
### **Symptoms**
  - "Our loop metrics look great but growth is flat"
  - High vanity numbers, low actual conversion
  - Can't explain growth with loop metrics
### **Detection Pattern**
loop metrics|viral coefficient|k.factor

## Single Loop Dependency

### **Id**
single-loop-dependency
### **Summary**
Over-relying on one growth loop
### **Severity**
high
### **Situation**
Growth collapses when loop underperforms
### **Why**
  All loops eventually saturate.
  Platform changes can break loops.
  Competition copies successful loops.
  
### **Solution**
  ## Loop Portfolio Strategy
  
  ### Risk Assessment by Loop Type
  
  | Loop Type | Platform Risk | Competition Risk | Saturation Risk |
  |-----------|---------------|------------------|-----------------|
  | SEO Content | Medium (algorithm) | High (copyable) | Medium |
  | Paid | High (costs rise) | High (bid wars) | High |
  | Viral/Referral | Low | Medium | Low |
  | Product/Network | Low | Low | Low |
  
  ### Portfolio Approach
  
  **Stage 1: Dominant Loop**
  - Focus on one loop to prove it works
  - Get to 60%+ of growth from one loop
  - Deeply understand mechanics
  
  **Stage 2: Secondary Loop**
  - Add second loop from different category
  - Target 25-30% of growth
  - Provides hedge if primary weakens
  
  **Stage 3: Maintenance Loops**
  - Add 2-3 smaller loops (5-10% each)
  - Different risk profiles
  - Experiments for future primaries
  
  ### Loop Diversification Matrix
  ```
  High platform dependency → Low platform dependency
  High competition exposure → Low competition exposure
  
  Example portfolio:
  - Primary: Product loop (low risk) - 50%
  - Secondary: Content loop (medium risk) - 30%
  - Tertiary: Paid loop (high risk) - 15%
  - Experimental: New loops - 5%
  ```
  
  ### Early Warning Signals
  - Loop efficiency declining 3+ weeks
  - CAC rising faster than LTV
  - Channel policy changes announced
  - Competitors gaining in same loop
  
### **Symptoms**
  - Growth drops suddenly
  - Single channel drives >80% of acquisition
  - No backup plan when loop struggles
### **Detection Pattern**
loop portfolio|diversif|backup

## Loop Cycle Blindness

### **Id**
loop-cycle-blindness
### **Summary**
Ignoring cycle time in loop optimization
### **Severity**
medium
### **Situation**
Loop with good K-factor grows slowly
### **Why**
  K-factor gets all attention.
  Cycle time often more impactful.
  Faster cycles compound faster.
  
### **Solution**
  ## Cycle Time Optimization
  
  ### The Math of Cycle Time
  
  Growth over time with same K-factor:
  ```
  K = 1.2, 30-day cycle, 90 days:
  Cycles = 3 → Growth = 1.2³ = 1.73× original
  
  K = 1.2, 7-day cycle, 90 days:
  Cycles = 13 → Growth = 1.2¹³ = 10.7× original
  ```
  
  **6× faster cycle = 6× more growth**
  
  ### Cycle Time Audit
  
  Map each stage of your loop:
  1. Trigger (user reaches share point): X days from signup
  2. Action (user actually shares): X hours from trigger
  3. View (recipient sees share): X hours from action
  4. Convert (recipient signs up): X hours from view
  
  Total cycle time = Sum of all stages
  
  ### Reduction Strategies
  
  | Stage | Reduction Tactic |
  |-------|------------------|
  | Trigger | Faster time-to-value, earlier share moment |
  | Action | Pre-filled content, one-click share |
  | View | Push notifications, email, real-time |
  | Convert | Frictionless signup, mobile-optimized |
  
  ### Cycle Time Benchmarks
  
  | Loop Type | Fast | Average | Slow |
  |-----------|------|---------|------|
  | Referral | 1-3 days | 7-14 days | 30+ days |
  | Content | Hours | 1-7 days | Weeks |
  | Product/Collab | Minutes | Hours | Days |
  
### **Symptoms**
  - Good K-factor but slow growth
  - Competitors with worse K growing faster
  - Long time between signup and first share
### **Detection Pattern**
cycle time|time to|days to share

## Quality Quantity Tradeoff

### **Id**
quality-quantity-tradeoff
### **Summary**
Optimizing loop volume over quality
### **Severity**
medium
### **Situation**
Loop brings users who don't retain
### **Why**
  Easy to measure quantity.
  Quality takes longer to assess.
  Short-term metrics look good.
  
### **Solution**
  ## Loop Quality Framework
  
  ### Quality Metrics by Loop
  
  **Referral Loop Quality**
  - Day 7/30/90 retention of referred vs organic
  - LTV of referred vs organic
  - Activation rate of referred users
  - Referred user NPS
  
  **Content Loop Quality**
  - Time on site from loop-acquired
  - Signup rate from loop visitors
  - Retention of loop-acquired signups
  - Content engagement depth
  
  **Paid Loop Quality**
  - Payback period by source/campaign
  - LTV:CAC by cohort
  - Retention by acquisition source
  - Feature adoption by source
  
  ### Quality Gates
  
  Don't scale loops until:
  - 14-day retention ≥ 80% of organic baseline
  - Activation rate ≥ 70% of organic
  - 90-day LTV ≥ 60% of organic
  
  ### Quality Optimization
  
  **Referral**: Screen referred users with qualification
  **Content**: Target high-intent keywords/topics
  **Paid**: Tighten targeting, accept higher CAC
  
  Trade volume for quality when:
  - Loop-acquired retention < 50% of organic
  - CAC payback exceeds 18 months
  - NPS from loop users is negative
  
### **Symptoms**
  - High acquisition, low retention
  - Growing users but not revenue
  - Loop-acquired users churn faster
### **Detection Pattern**
quality|retention|ltv.*cac

## Loop Measurement Lag

### **Id**
loop-measurement-lag
### **Summary**
Making decisions before loop data matures
### **Severity**
medium
### **Situation**
Killed working loop or scaled broken one
### **Why**
  Loops take time to complete cycles.
  Early data is misleading.
  Pressure to show quick results.
  
### **Solution**
  ## Loop Measurement Patience
  
  ### Minimum Measurement Periods
  
  | Loop Type | Min Cycles | Typical Time |
  |-----------|------------|--------------|
  | Viral/Referral | 3 cycles | 2-6 weeks |
  | Content/SEO | 2-3 cycles | 4-12 weeks |
  | Paid | 2-3 cohorts | 4-8 weeks |
  | Product | 3-5 usage cycles | Varies |
  
  ### Early Indicators (Directional Only)
  
  While waiting for full loop data:
  - Referral: Invite acceptance rate (first 48h)
  - Content: Initial indexing, early impressions
  - Paid: Cost per click, landing page conversion
  
  These are NOT loop metrics - just early signals
  
  ### Decision Framework
  
  **Week 1-2**: Only fix obvious breaks
  **Week 3-4**: Optimize individual stages
  **Week 5+**: Make loop-level decisions
  **Week 8+**: Scale or kill decisions
  
  ### Common Premature Decisions
  
  ❌ "Referral isn't working" (Day 5)
  → Wait for 2+ full cycles
  
  ❌ "Content loop is slow" (Week 2)
  → SEO loops take 8-12 weeks minimum
  
  ❌ "Paid CAC is too high" (Week 1)
  → Wait for LTV data to calculate true CAC:LTV
  
### **Symptoms**
  - Constantly changing loop strategy
  - Conflicting conclusions week-to-week
  - Killed initiatives that needed more time
### **Detection Pattern**
measure|wait|too early