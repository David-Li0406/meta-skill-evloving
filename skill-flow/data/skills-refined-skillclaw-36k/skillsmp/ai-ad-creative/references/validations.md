# Ai Ad Creative - Validations

## Ad copy must not make unsubstantiated claims

### **Id**
no-unsubstantiated-claims
### **Severity**
critical
### **Description**
Advertising claims need evidence or disclaimers
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py,yaml,md}
  #### **Match**
ad.*(guarantee|proven|will make|definitely|always works)
  #### **Exclude**
disclaimer|typical|may|can|results vary
### **Message**
Ad copy may contain unsubstantiated claims. Add disclaimer or revise.
### **Autofix**


## Ads must specify platform-appropriate dimensions

### **Id**
platform-specs-checked
### **Severity**
critical
### **Description**
Wrong dimensions cause rejection or poor performance
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
(create|generate).*ad.*image
  #### **Exclude**
(1:1|4:5|9:16|16:9)|aspect|ratio|size|dimension|platform
### **Message**
Ad generation without dimension specification. Add platform-specific aspect ratio.
### **Autofix**


## AI-generated ads may require disclosure

### **Id**
disclosure-for-ai-content
### **Severity**
high
### **Description**
Some platforms require labeling AI-generated content
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
(publish|upload|launch).*ad.*(ai|generated|synthetic)
  #### **Exclude**
disclosure|label|ai.generated|synthetic.media
### **Message**
Publishing AI-generated ad without disclosure check. Verify platform requirements.
### **Autofix**


## Video ad prompts should specify hook

### **Id**
hook-in-prompt
### **Severity**
high
### **Description**
First 3 seconds are critical for video ads
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py,yaml}
  #### **Match**
(video|ad|tiktok|reel).*prompt
  #### **Exclude**
hook|first.*second|opening|attention|scroll.stop
### **Message**
Video ad without hook specification. Define first 3 seconds strategy.
### **Autofix**


## Ads should have clear call-to-action

### **Id**
cta-specified
### **Severity**
medium
### **Description**
Ads without CTA don't drive action
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py,yaml}
  #### **Match**
ad.*(copy|text|message)
  #### **Exclude**
CTA|call.to.action|shop.now|learn.more|sign.up|get.started
### **Message**
Ad copy without CTA. Add clear call-to-action.
### **Autofix**


## A/B tests should isolate single variable

### **Id**
single-variable-test
### **Severity**
medium
### **Description**
Multiple variable changes invalidate test results
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
test.*variant|ab.test|split.test
  #### **Exclude**
single.*variable|isolate|one.*change|control
### **Message**
A/B test may change multiple variables. Isolate single variable for valid results.
### **Autofix**


## Ad campaign should have refresh strategy

### **Id**
refresh-pipeline-exists
### **Severity**
medium
### **Description**
Creative fatigue requires proactive refresh
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
campaign|ad.strategy
  #### **Exclude**
refresh|fatigue|new.*creative|variant|pipeline
### **Message**
Campaign without refresh strategy. Plan for creative fatigue.
### **Autofix**


## New creative should have limited test budget

### **Id**
testing-budget-limited
### **Severity**
medium
### **Description**
Unproven creative shouldn't get full spend
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
launch.*ad|new.*creative.*budget
  #### **Exclude**
test|limited|small|trial|minimum
### **Message**
Launching creative without test budget limits. Start small, scale winners.
### **Autofix**


## Ad creative should match brand guidelines

### **Id**
brand-consistency-check
### **Severity**
medium
### **Description**
Performance ads should still be on-brand
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py,yaml}
  #### **Match**
(generate|create).*ad
  #### **Exclude**
brand|style|guidelines|colors|font
### **Message**
Ad generation without brand reference. Include brand guidelines in prompt.
### **Autofix**


## Ads should have conversion tracking

### **Id**
performance-tracking
### **Severity**
high
### **Description**
Without tracking, you can't optimize
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
launch|publish.*ad
  #### **Exclude**
track|pixel|conversion|analytics|utm
### **Message**
Launching ad without tracking reference. Ensure conversion tracking is set up.
### **Autofix**


## Ad tests should be documented for learning

### **Id**
test-documentation
### **Severity**
low
### **Description**
Undocumented tests waste learning opportunities
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
test.*complete|test.*result
  #### **Exclude**
document|log|record|save.*learning
### **Message**
Test completion without documentation. Record learnings for future use.
### **Autofix**


## Ads should be adapted per platform

### **Id**
platform-native-content
### **Severity**
medium
### **Description**
Generic ads underperform vs platform-native
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
(meta|tiktok|linkedin|youtube).*same.*creative
  #### **Exclude**
adapt|native|platform.specific|recreate
### **Message**
Using same creative across platforms. Adapt for each platform context.
### **Autofix**


## Social ads should consider UGC-style

### **Id**
ugc-style-for-social
### **Severity**
low
### **Description**
Authentic content often outperforms polished
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py,yaml}
  #### **Match**
(tiktok|instagram|facebook).*ad.*polished|professional.*ad
  #### **Exclude**
ugc|authentic|native|casual|organic
### **Message**
Social ad may be too polished. Consider UGC-style for better performance.
### **Autofix**
