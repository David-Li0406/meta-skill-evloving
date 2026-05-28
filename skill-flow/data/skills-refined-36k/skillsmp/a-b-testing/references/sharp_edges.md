# A B Testing - Sharp Edges

## Peeking Problem

### **Id**
peeking-problem
### **Summary**
Checking results before planned sample size and stopping early
### **Severity**
critical
### **Situation**
  Impatience. Pressure to ship. Results look "obviously" significant after 3 days.
  "We already have 10,000 users, that's enough."
  
### **Why**
  Statistical significance fluctuates wildly early in experiments. Peeking
  dramatically inflates false positive rates—what looks like 5% significance
  becomes 30%+. You'll declare winners that aren't winners.
  
### **Solution**
  # Pre-commit to sample size and duration:
  Calculate required sample size before starting
  Set end date and stick to it
  
  # Use sequential testing methods if early stopping required:
  Bayesian methods
  Always Valid Inference
  Built-in peeking correction
  
  # Don't look at primary metrics until experiment ends:
  Check only for technical issues
  Automate experiment completion
  
  # Example:
  "Experiment runs until [date] or [sample size]"
  No early stopping based on results
  
### **Symptoms**
  - Checking results daily
  - Stopping when "it looks significant"
  - Different experiment durations
  - High rate of "winning" experiments
### **Detection Pattern**


## Underpowered Tests

### **Id**
underpowered-tests
### **Summary**
Running experiments without enough sample size to detect meaningful effects
### **Severity**
critical
### **Situation**
  Testing on 500 users to detect a 2% lift. "We'll just run it longer if needed."
  Small user base. Impatience.
  
### **Why**
  Underpowered tests usually show no effect—not because there isn't one,
  but because you couldn't detect it. You'll kill good ideas that actually work.
  Or worse, p-hack to "find" effects.
  
### **Solution**
  # Always calculate required sample size before starting:
  Know your baseline conversion rate
  Define minimum detectable effect (MDE)
  Calculate power (usually 80%)
  
  # Power calculation:
  Sample size = f(baseline, MDE, significance, power)
  Many online calculators available
  
  # If you can't reach required sample size:
  - Accept a larger MDE
  - Don't run the test
  - Use Bayesian methods for smaller samples
  
  # Never:
  "Let's just see what happens"
  "We'll run it longer if needed"
  
### **Symptoms**
  - No power analysis before test
  - Tests frequently inconclusive
  - Small sample sizes
  - MDE not defined
### **Detection Pattern**


## Multiple Comparison Inflation

### **Id**
multiple-comparison-inflation
### **Summary**
Testing many metrics without adjusting for multiple comparisons
### **Severity**
high
### **Situation**
  Running 20 metrics on each experiment. "More metrics = more learning."
  Celebrating the one that's significant. Cherry-picking favorable results.
  
### **Why**
  With 20 metrics at 5% significance level, you expect 1 false positive by
  pure chance. That "significant" metric might be noise. You'll ship changes
  that actually hurt because one random metric looked good.
  
### **Solution**
  # Pre-register primary metrics:
  1-2 primary metrics that matter
  Hypothesis stated upfront
  
  # Apply corrections for multiple comparisons:
  Bonferroni: α / number of tests
  Benjamini-Hochberg: Controls false discovery rate
  Both reduce false positives
  
  # Distinguish analysis types:
  Confirmatory: Hypothesis-testing (strict)
  Exploratory: Hypothesis-generating (looser)
  
  # Example:
  Primary: Conversion rate (α = 0.05)
  Secondary: 10 other metrics (exploratory only)
  
### **Symptoms**
  - Many metrics tested without correction
  - Cherry-picking significant results
  - Primary metric not pre-registered
  - Post-hoc storytelling
### **Detection Pattern**


## Sample Ratio Mismatch

### **Id**
sample-ratio-mismatch
### **Summary**
Not validating that experiment splits traffic correctly
### **Severity**
critical
### **Situation**
  Assuming 50/50 split is actually 50/50. Trust the tooling.
  Don't check. Assignment bugs invisible without monitoring.
  
### **Why**
  SRM indicates broken randomization. Groups aren't comparable.
  Any observed difference might be from broken assignment, not treatment.
  Results are uninterpretable.
  
### **Solution**
  # Always check sample ratio before analyzing:
  Expected: 50/50
  Actual: 48/52
  Is this significant deviation?
  
  # Alert on significant deviations:
  Chi-square test for SRM
  Investigate any SRM before trusting results
  
  # Common SRM causes:
  - Bot traffic
  - Caching issues
  - Assignment bugs
  - Redirect handling
  
  # Example check:
  if (abs(actual_split - expected_split) > threshold) {
    alert("Sample ratio mismatch detected")
    investigate before analyzing
  }
  
### **Symptoms**
  - Never checking split ratio
  - Uneven splits accepted
  - Bot traffic not filtered
  - Results trusted without validation
### **Detection Pattern**


## Carryover Effects

### **Id**
carryover-effects
### **Summary**
Not accounting for users experiencing multiple variants over time
### **Severity**
high
### **Situation**
  Running experiments too long. Testing on same users repeatedly.
  Features change over time. Users develop habits with first experience.
  
### **Why**
  Users develop habits with first experience. Novelty effects fade.
  A "better" variant might only be better because it's new.
  Long-running experiments accumulate external changes.
  
### **Solution**
  # Account for novelty effects:
  Initial lifts often fade
  Check 2-week vs 4-week results
  
  # Use holdout groups for long-term effects:
  Keep control group for extended period
  Measure true long-term impact
  
  # Be cautious with experiments on repeat behaviors:
  User habits matter
  First experience shapes perception
  
  # Consider experiment design:
  Between-subjects: Each user sees one variant
  Within-subjects: Users see multiple (more complex)
  
### **Symptoms**
  - Experiments running for months
  - Same users in multiple tests
  - Novelty not considered
  - No long-term validation
### **Detection Pattern**


## Selection Bias Assignment

### **Id**
selection-bias-assignment
### **Summary**
Assigning users to variants in ways that create systematic differences
### **Severity**
critical
### **Situation**
  Using user ID mod for assignment when IDs aren't random.
  Simple assignment seems fine. Technical constraints lead to non-random approaches.
  
### **Why**
  Groups differ before experiment starts. Treatment and control aren't comparable.
  You're measuring pre-existing differences, not treatment effects.
  
### **Solution**
  # Use proper randomization:
  Hashing with salt
  Not: user_id % 2
  But: hash(user_id + experiment_salt) % 100
  
  # Validate covariate balance:
  Check for pre-treatment differences
  Compare groups on key metrics before experiment
  
  # Use stratified randomization for small samples:
  Ensure balance on important characteristics
  Block randomization
  
  # Example validation:
  Compare control vs treatment on:
  - Demographics
  - Historical behavior
  - Pre-experiment metrics
  Should be statistically similar
  
### **Symptoms**
  - Simple modulo assignment
  - No balance checking
  - Systematic group differences
  - Assignment not truly random
### **Detection Pattern**


## Survivor Bias Analysis

### **Id**
survivor-bias-analysis
### **Summary**
Analyzing only users who complete a flow, ignoring dropouts
### **Severity**
high
### **Situation**
  "Conversion rate among users who saw the checkout page."
  Analyzing only complete cohorts. Drop-offs seem like different problem.
  
### **Why**
  You're conditioning on a post-treatment outcome. If your variant causes
  more people to reach checkout, the survivors are different populations.
  Comparisons are invalid.
  
### **Solution**
  # Use intent-to-treat analysis:
  Analyze ALL users assigned
  Not just those who completed
  
  # Track the full funnel:
  Start: All assigned users
  Each step: Track drop-off
  End: Completed users
  
  # Subgroup rules:
  Ensure subgroup definition can't be affected by treatment
  If variant affects who reaches step, don't compare at that step
  
  # Example:
  Not: "Conversion rate of checkout viewers"
  But: "Conversion rate of all experiment participants"
  
### **Symptoms**
  - Analyzing only completers
  - Funnel analysis on post-treatment segments
  - Drop-offs not tracked
  - Invalid subgroup comparisons
### **Detection Pattern**


## Network Effects Ignorance

### **Id**
network-effects-ignorance
### **Summary**
User-level randomization when features have network effects
### **Severity**
high
### **Situation**
  Running user-level randomization on social/collaborative features.
  User randomization is standard. Don't think about user interactions.
  
### **Why**
  Users in treatment affect users in control (and vice versa).
  Effects spill over. Measured effect underestimates (or overestimates)
  true effect of full rollout.
  
### **Solution**
  # Use cluster randomization:
  By geography
  By workplace
  By network cluster
  
  # Run switchback experiments:
  Time-based randomization
  All users get same treatment in each period
  
  # Model and account for interference:
  Estimate spillover effects
  Adjust analysis accordingly
  
  # When in doubt:
  Run regional rollouts
  Compare regions, not users
  
### **Symptoms**
  - User-level tests on social features
  - Collaboration features tested individually
  - Network effects ignored
  - Spillover not considered
### **Detection Pattern**


## Local Maximum Chasing

### **Id**
local-maximum-chasing
### **Summary**
Only running incremental tests, missing fundamental improvements
### **Severity**
high
### **Situation**
  A/B testing button colors while entire flow is wrong.
  Small tests are safe. Big changes scary. Incremental feels productive.
  
### **Why**
  You'll optimize to local maximum while missing global maximum.
  Thousands of small tests can't find what one bold test would reveal.
  Polishing a suboptimal design.
  
### **Solution**
  # Balance incremental with bold:
  80% optimization tests
  20% exploration tests
  
  # Periodically test radical approaches:
  Completely different designs
  Question the fundamentals
  
  # Use holdout groups:
  Measure cumulative effect of optimizations
  Are small wins adding up?
  
  # Ask bigger questions:
  Not: "Which button color?"
  But: "Should this be a button at all?"
  
### **Symptoms**
  - Only testing small changes
  - Never questioning fundamentals
  - Optimizing wrong things
  - No big wins despite many tests
### **Detection Pattern**


## Metric Definition Drift

### **Id**
metric-definition-drift
### **Summary**
Changing metric definitions mid-experiment or across experiments
### **Severity**
high
### **Situation**
  "This metric definition is better." Discovered issue with current definition.
  Different teams use different definitions.
  
### **Why**
  Can't compare pre/post changes. Historical learnings invalid.
  Different experiments can't be compared. Optimizing different things
  than you think.
  
### **Solution**
  # Lock metric definitions before experiment starts:
  Document in code or SQL, not prose
  Version definitions
  
  # Use a metrics layer:
  Single source of truth
  All experiments use same definitions
  
  # If you must change definitions:
  Clearly mark the break in continuity
  Don't compare across the break
  Rerun historical analysis with new definition
  
  # Document precisely:
  "Active user = logged in within 7 days"
  Not: "Active user = engaged user"
  
### **Symptoms**
  - Metric definitions change mid-test
  - Different teams use different definitions
  - Can't compare historical experiments
  - Definitions in prose, not code
### **Detection Pattern**


## Winners Curse

### **Id**
winners-curse
### **Summary**
Trusting observed effect size of winning experiment as true effect
### **Severity**
high
### **Situation**
  "We saw a 15% lift, so we'll plan for 15%."
  The number is right there. Significant means real.
  
### **Why**
  Winning experiments have upward-biased effect estimates—you selected
  them because they showed large effects. True effects typically
  20-50% smaller. Projections will disappoint.
  
### **Solution**
  # Expect effect shrinkage:
  Observed effect: 15%
  Expected true effect: 8-12%
  
  # Use holdout groups:
  Validate long-term impact
  Compare to projection
  
  # Build in conservatism:
  Don't bet on point estimates
  Use ranges for projections
  
  # Example planning:
  Observed: +15%
  Plan for: +8-10%
  Build scenarios for +5% and +12%
  
### **Symptoms**
  - Planning based on point estimates
  - No effect shrinkage expected
  - Projections consistently miss
  - No long-term validation
### **Detection Pattern**


## Guardrail Negligence

### **Id**
guardrail-negligence
### **Summary**
Only measuring target metric, ignoring broader impact
### **Severity**
critical
### **Situation**
  Focus on the goal metric only. Guardrails seem like extra work.
  "What could go wrong?"
  
### **Why**
  Improve clicks while destroying engagement. Increase signups while
  tanking retention. Win on one metric, lose on everything else.
  Ship changes that hurt the business overall.
  
### **Solution**
  # Define guardrail metrics before every experiment:
  Revenue (or proxy)
  Engagement depth
  User satisfaction
  Technical performance (latency, errors)
  
  # Treat guardrail failures as experiment failures:
  Even if primary metric wins
  Can't ship if guardrails fail
  
  # Example guardrails:
  Primary: Signup rate
  Guardrails:
  - D7 retention ≥ baseline
  - Session length ≥ baseline
  - Error rate ≤ baseline
  - Page load ≤ baseline
  
### **Symptoms**
  - Only tracking primary metric
  - No guardrails defined
  - Shipped tests that hurt overall
  - No quality/engagement checks
### **Detection Pattern**
