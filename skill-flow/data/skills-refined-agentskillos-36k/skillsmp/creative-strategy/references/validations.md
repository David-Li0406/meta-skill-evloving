# Creative Strategy - Validations

## No Creative Brief Defined

### **Id**
creative-no-brief
### **Severity**
error
### **Type**
regex
### **Pattern**
  - campaign|creative|concept|execution|design
### **Message**
Creative work mentioned without a brief. No brief = no strategy. You're guessing.
### **Fix Action**
Create brief first: objective, target audience, key message, tone, success metrics, constraints
### **Applies To**
  - *.md
  - *.txt
  - README*

## Target Audience Undefined

### **Id**
creative-no-target
### **Severity**
error
### **Type**
regex
### **Pattern**
  - message|messaging|communication|content
### **Message**
Messaging without defined target audience. Who are you talking to? Be specific.
### **Fix Action**
Define audience: demographics, psychographics, pain points, media consumption, language they use
### **Applies To**
  - *.md
  - *.txt

## Tactics Before Strategy

### **Id**
creative-tactics-first
### **Severity**
error
### **Type**
regex
### **Pattern**
  - video|ad|post|email|banner|landing.?page|social.?media
### **Message**
Jumping to tactics before strategy. Channels are not strategy. Why before how.
### **Fix Action**
Define strategy first: What behavior change? What message? What emotional response? Then choose channels.
### **Applies To**
  - *.md
  - *.txt

## No Clear Creative Objective

### **Id**
creative-no-objective
### **Severity**
error
### **Type**
regex
### **Pattern**
  - creative|campaign|content
### **Message**
Creative work without clear objective. Awareness? Consideration? Conversion? Pick one primary goal.
### **Fix Action**
State objective explicitly: Is this to inform, persuade, or activate? What specific action do you want?
### **Applies To**
  - *.md
  - *.txt

## Multiple Key Messages

### **Id**
creative-multiple-messages
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - and.?also|as.?well.?as|in.?addition|furthermore|plus
### **Message**
Multiple messages detected. One creative execution = one key message. More messages = less impact.
### **Fix Action**
Choose ONE key message: What is the single most important thing your audience must remember?
### **Applies To**
  - *.md
  - *.txt

## No Consumer Insight

### **Id**
creative-no-insight
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - target|audience|customer|user
### **Message**
No consumer insight mentioned. Great creative is built on truth about human behavior, not demographics.
### **Fix Action**
Find the insight: What do they believe? What do they fear? What do they want but won't admit?
### **Applies To**
  - *.md
  - *.txt

## Tone By Committee

### **Id**
creative-committee-tone
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - professional.?yet.?fun|serious.?but.?approachable|friendly.?and.?expert
### **Message**
Contradictory tone language. 'Professional yet fun' is mush. Pick a side. Strong tone has opinion.
### **Fix Action**
Choose ONE tone: Are you the expert, the friend, the rebel, the helper? Commit fully.
### **Applies To**
  - *.md
  - *.txt

## No Clear Call to Action

### **Id**
creative-no-call-to-action
### **Severity**
error
### **Type**
regex
### **Pattern**
  - creative|campaign|ad|content
### **Message**
Creative without clear CTA. What should they do next? Make it impossible to miss.
### **Fix Action**
Define ONE clear action: Click, sign up, buy, share, comment? One primary CTA only.
### **Applies To**
  - *.md
  - *.txt

## Playing It Safe

### **Id**
creative-safe-language
### **Severity**
info
### **Type**
regex
### **Pattern**
  - appropriate|suitable|acceptable|reasonable|balanced|moderate
### **Message**
Safe language detected. Safe creative doesn't get noticed. Breakthrough work polarizes.
### **Fix Action**
Take a stance: What will make some people love this and others hate it? Aim for that edge.
### **Applies To**
  - *.md
  - *.txt

## No Creative Constraints

### **Id**
creative-no-constraints
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - anything|unlimited|freedom|open|flexible
### **Message**
No constraints mentioned. Constraints drive creativity. Unlimited options = paralysis.
### **Fix Action**
Set constraints: budget, timeline, format, channel, length, brand guidelines. Limits unlock ideas.
### **Applies To**
  - *.md
  - *.txt

## Awards Over Effectiveness

### **Id**
creative-awards-focus
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - award|win|recognition|industry|showcase|portfolio
### **Message**
Award-focused language. Creative that wins awards often fails business objectives. Choose your master.
### **Fix Action**
Focus on business results: What metric moves? Sales, signups, retention? Award winning is a bonus.
### **Applies To**
  - *.md
  - *.txt

## No Testing or Iteration Plan

### **Id**
creative-no-testing-plan
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - launch|publish|release|go.?live
### **Message**
Launching without testing plan. Never launch one version. Test variants, learn, iterate.
### **Fix Action**
Plan tests: A/B test headlines, visuals, CTAs. Define success metrics. Set iteration timeline.
### **Applies To**
  - *.md
  - *.txt