# Brand Storytelling - Validations

## Story hero should be customer, not brand

### **Id**
hero-is-customer
### **Severity**
critical
### **Description**
Brand as hero creates disconnection
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py,yaml,md}
  #### **Match**
(our|we|brand).*hero|hero.*brand|(our|we).*save
  #### **Exclude**
customer.*hero|user.*hero|mentor|guide
### **Message**
Story may position brand as hero. Customer should be protagonist, brand as mentor.
### **Autofix**


## Story should have clear conflict or stakes

### **Id**
conflict-exists
### **Severity**
high
### **Description**
Stories without conflict don't engage
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
story|narrative|testimonial|case.*study
  #### **Exclude**
conflict|challenge|struggle|problem|obstacle|stake
### **Message**
Story may lack conflict. Add clear stakes and challenges.
### **Autofix**


## Story should show clear transformation

### **Id**
transformation-clear
### **Severity**
high
### **Description**
Stories need before/after change
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
story|narrative|customer.*story
  #### **Exclude**
transform|before.*after|change|result|outcome
### **Message**
Story may lack clear transformation. Show before/after change.
### **Autofix**


## Story should have specific details

### **Id**
specificity-present
### **Severity**
high
### **Description**
Generic stories don't stick
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
story|case.*study|testimonial
  #### **Exclude**
specific|name|number|date|quote|detail
### **Message**
Story may lack specificity. Add names, numbers, dates, quotes.
### **Autofix**


## Story should have emotional progression

### **Id**
emotional-arc-planned
### **Severity**
medium
### **Description**
Stories should move through emotions
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
story.*structure|narrative.*design
  #### **Exclude**
emotion|feel|arc|journey|progression
### **Message**
Story may lack emotional arc. Plan emotional progression.
### **Autofix**


## Brand storytelling should have documented narrative

### **Id**
story-bible-exists
### **Severity**
medium
### **Description**
Consistency requires documentation
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
brand.*story|storytelling|narrative
  #### **Exclude**
bible|document|guide|framework|core.*narrative
### **Message**
Brand storytelling without story bible. Document core narrative.
### **Autofix**


## Story should show rather than tell

### **Id**
show-not-tell
### **Severity**
medium
### **Description**
Showing beats telling for credibility
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
we.*are|our.*is.*best|innovative|leader
  #### **Exclude**
story|example|case|demonstrate
### **Message**
May be telling instead of showing. Use stories to demonstrate claims.
### **Autofix**


## Stories should integrate data for credibility

### **Id**
data-story-integrated
### **Severity**
medium
### **Description**
Story needs proof; data needs context
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
story|narrative|testimonial
  #### **Exclude**
data|number|percent|metric|proof
### **Message**
Story may lack data integration. Add quantifiable proof.
### **Autofix**


## Story should be adaptable to different formats

### **Id**
format-adaptation-planned
### **Severity**
low
### **Description**
One story, many formats
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
story|narrative
  #### **Exclude**
format|adapt|long.*form|short|variation
### **Message**
Story may not be planned for format adaptation. Consider multiple formats.
### **Autofix**


## Story should consider target audience

### **Id**
audience-considered
### **Severity**
low
### **Description**
Stories should be audience-aware
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
story|narrative|brand.*story
  #### **Exclude**
audience|persona|target|who
### **Message**
Story may not consider audience. Define who this story is for.
### **Autofix**


## Story variations should be tracked for consistency

### **Id**
consistency-tracked
### **Severity**
low
### **Description**
Multiple versions need consistency check
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
story|narrative|publish
  #### **Exclude**
consistent|version|track|bible
### **Message**
Publishing story without consistency tracking. Review against story bible.
### **Autofix**
