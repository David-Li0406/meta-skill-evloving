# A/B Testing

## Patterns


---
  #### **Name**
Hypothesis-First Design
  #### **Description**
Write specific, falsifiable hypotheses before building variants
  #### **When**
Starting any experiment design
  #### **Example**
    Bad: "Let's test a green button"
    Good: "Changing CTA from 'Learn More' to 'Start Free Trial' will increase
    conversion by 15% because users want clarity about the next step"
    
    Components of good hypothesis:
    - What we're changing (CTA text)
    - What we expect to happen (15% lift in conversion)
    - Why we believe this (users want clarity)
    - How we'll measure it (conversion rate)
    

---
  #### **Name**
Sample Size Pre-Commitment
  #### **Description**
Calculate and commit to sample size before starting test
  #### **When**
Before launching any experiment
  #### **Example**
    # Use power analysis to determine minimum sample size
    baseline_rate = 0.05  # 5% conversion
    mde = 0.15           # 15% relative improvement (to 5.75%)
    power = 0.80         # 80% chance of detecting if real
    alpha = 0.05         # 5% false positive rate
    
    # Result: Need 12,400 users per variant
    # Run until both variants reach 12,400, not until "it looks significant"
    
    Never peek at results and stop early when winning - this inflates false positives.
    

---
  #### **Name**
Guardrail Metrics Shield
  #### **Description**
Monitor secondary metrics to catch unintended harm
  #### **When**
Running any experiment that could have negative side effects
  #### **Example**
    Primary: Increase sign-up conversion
    Guardrails:
    - Time to complete sign-up (catch if we made it confusing)
    - Day 7 retention (catch if we're attracting wrong users)
    - Support ticket rate (catch if variant creates confusion)
    - Page load time (catch if variant breaks performance)
    
    Ship only if: Primary improves AND no guardrails regress beyond threshold
    

---
  #### **Name**
Segmented Analysis
  #### **Description**
Analyze results by user segments to find hidden patterns
  #### **When**
After gathering sufficient sample size
  #### **Example**
    Overall result: +2% conversion (not significant)
    
    Segmented analysis reveals:
    - Mobile: +15% conversion (highly significant)
    - Desktop: -8% conversion (significant)
    
    Decision: Ship to mobile only, iterate on desktop variant
    
    Common segments: device type, new vs returning, geography, referral source
    

---
  #### **Name**
Sequential Testing
  #### **Description**
Use sequential testing for high-traffic experiments that need fast decisions
  #### **When**
Testing on high-volume flows where waiting for fixed sample is costly
  #### **Example**
    Instead of: "Wait for 10,000 users per variant"
    Use: Sequential probability ratio test that checks after every 100 conversions
    
    Allows: Stopping early when effect is clear (winner or no difference)
    Prevents: False positives through adjusted significance boundaries
    
    Tools: Optimizely's Stats Engine, Evan Miller's sequential calculator
    

---
  #### **Name**
Iteration Over Validation
  #### **Description**
When tests fail, analyze and iterate rather than just validating failure
  #### **When**
Test shows negative or neutral result
  #### **Example**
    Test failed: New checkout flow reduced conversions by 3%
    
    Bad response: "Test failed, revert and move on"
    Good response:
    1. Analyze: Where in flow did users drop off?
    2. Hypothesis: Too many form fields scared mobile users
    3. Iterate: Test simplified mobile-specific variant
    4. Result: +12% mobile conversion
    
    Failed tests contain the seeds of winning tests.
    

## Anti-Patterns


---
  #### **Name**
Testing Without Hypothesis
  #### **Description**
Running experiments with vague goals like "see what performs better"
  #### **Why**
You can't learn from results if you don't know what you were testing
  #### **Instead**
    Write hypothesis first: "If [change], then [outcome] because [reasoning]"
    This forces you to articulate assumptions that you can validate or invalidate
    

---
  #### **Name**
Peeking and Stopping Early
  #### **Description**
Checking results daily and stopping test when it looks significant
  #### **Why**
    Massively inflates false positive rate. With enough peeks, random noise
    will eventually look significant. Your 5% false positive rate becomes 30%+
    
  #### **Instead**
    Pre-commit to sample size. Only look at results after reaching it.
    Or use sequential testing with proper alpha spending adjustments
    

---
  #### **Name**
Testing Too Many Things
  #### **Description**
Multivariate tests with 5+ variables creating 32+ combinations
  #### **Why**
    Sample size required grows exponentially. You'll either run test for months
    or stop with underpowered results. Interactions make results uninterpretable
    
  #### **Instead**
    Test one thing at a time. Or use staged rollout: test A, ship winner, test B.
    Save multivariate for high-traffic flows where you can reach power quickly
    

---
  #### **Name**
Ignoring Novelty Effects
  #### **Description**
Calling test after 2 days when existing users haven't adjusted to change
  #### **Why**
    Existing users often react negatively to any change initially (novelty effect)
    or positively to something new (novelty effect). Effect fades after 1-2 weeks
    
  #### **Instead**
    Run tests for minimum 1-2 weeks to let novelty effects stabilize.
    For major changes, analyze new users separately from existing users
    

---
  #### **Name**
Cargo Cult Significance
  #### **Description**
Blindly shipping any test that crosses p < 0.05 threshold
  #### **Why**
    Statistical significance doesn't mean practical significance. A "significant"
    0.1% improvement might cost more to implement than it generates. Also doesn't
    account for multiple comparisons or guardrail metric degradation
    
  #### **Instead**
    Set minimum practical significance threshold (e.g., +5% conversion minimum).
    Check guardrails. Adjust significance for multiple comparisons. Use judgment
    

---
  #### **Name**
Testing Without Traffic
  #### **Description**
Running A/B tests on flows with <1000 weekly users
  #### **Why**
    Will take months to reach statistical power. By then, product has changed,
    test is no longer relevant. Opportunity cost of not shipping is too high
    
  #### **Instead**
    On low-traffic: Ship with feature flag, monitor metrics, roll back if bad.
    Save rigorous A/B testing for high-traffic flows where you can reach power in days
    