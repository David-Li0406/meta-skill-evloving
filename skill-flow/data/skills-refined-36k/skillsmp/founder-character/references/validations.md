# Founder Character - Validations

## Victim Mindset Language

### **Id**
fc-victim-language
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - not.?fair|unfair|should.?have|deserve|entitled
  - they.?did.?this|it.?was.?done.?to|happened.?to.?us
  - if.?only|we.?had.?no.?choice|forced.?to
### **Message**
Victim language detected. Founders own outcomes, not circumstances. External blame is internal weakness.
### **Fix Action**
Reframe: 'The market did X to us' → 'We failed to anticipate market shift. Here is what we learned.'
### **Applies To**
  - *.md
  - *.txt

## Excuse-Making Pattern

### **Id**
fc-excuse-making
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - because.?of|due.?to|result.?of|caused.?by
  - we.?could.?not|we.?cannot|impossible|no.?way
### **Message**
Excuse pattern detected. Reasons are not results. Focus on what you can control.
### **Fix Action**
Replace excuse with action: 'We could not because X' → 'We will do Y instead'
### **Applies To**
  - *.md
  - *.txt

## Competitor Obsession

### **Id**
fc-competitor-obsession
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - competitor|competition|they.?are.?doing|beat.?them|winning.?against
### **Message**
Competitor-focused thinking detected. Build for customers, not against competitors.
### **Fix Action**
Refocus: What do customers need that is unserved? That is your opportunity.
### **Applies To**
  - *.md
  - *.txt

## Perfectionism Language

### **Id**
fc-perfection-paralysis
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - not.?ready|need.?to.?perfect|polish|refine.?before|almost.?there
  - just.?a.?few.?more|one.?more.?thing|not.?quite
### **Message**
Perfectionism detected. Shipping beats perfecting. Done is better than perfect.
### **Fix Action**
Ask: What is the minimum to learn? Ship that. Perfect later if validated.
### **Applies To**
  - *.md
  - *.txt

## Excessive Consensus Seeking

### **Id**
fc-consensus-seeking
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - everyone.?agrees|all.?aligned|unanimous|no.?disagreement
  - need.?buy-?in|wait.?for.?approval|get.?permission
### **Message**
Consensus-seeking detected. Good decisions often have disagreement. Waiting for everyone is waiting forever.
### **Fix Action**
Decide with input, not consensus. Communicate clearly, then act.
### **Applies To**
  - *.md
  - *.txt

## Cannot Delegate Language

### **Id**
fc-delegation-avoidance
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - only.?I.?can|no.?one.?else|have.?to.?do.?it.?myself|cannot.?delegate
  - I.?am.?the.?only|too.?important|critical.?that.?I
### **Message**
Delegation avoidance detected. If you are the only one who can do it, you are the bottleneck.
### **Fix Action**
Document, delegate, or eliminate. Your job is building the company, not doing all the work.
### **Applies To**
  - *.md
  - *.txt

## Overconfidence Without Evidence

### **Id**
fc-overconfidence
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - will.?definitely|guaranteed|certain|no.?doubt|obviously.?will
  - everyone.?wants|massive.?demand|huge.?market
### **Message**
Overconfident language without evidence. Confidence is earned through validation, not assertion.
### **Fix Action**
Add evidence: 'huge demand' → 'X customers paying, Y on waitlist, Z interview quotes'
### **Applies To**
  - *.md
  - *.txt

## Feature Obsession Over Customer

### **Id**
fc-feature-focus
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - feature|functionality|capability|we.?built|we.?added
### **Message**
Feature-focused language detected. Customers do not buy features. They buy outcomes.
### **Fix Action**
Translate features to outcomes: 'We built X' → 'Customers can now achieve Y'
### **Applies To**
  - *.md
  - *.txt

## Avoiding Hard Conversations

### **Id**
fc-avoiding-hard-conversations
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - not.?the.?right.?time|wait.?until|later|eventually|soon
  - sensitive|awkward|uncomfortable|difficult.?to.?discuss
### **Message**
Conversation avoidance detected. Delayed hard conversations become harder conversations.
### **Fix Action**
Schedule the conversation now. Direct is kind. Avoidance is cruel.
### **Applies To**
  - *.md
  - *.txt

## Vanity Metric Focus

### **Id**
fc-vanity-pursuit
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - press|media|awards|recognition|featured.?in|as.?seen|famous
  - followers|likes|impressions|viral
### **Message**
Vanity pursuit detected. Fame is not traction. Press is not product-market fit.
### **Fix Action**
Focus on metrics that matter: revenue, retention, customer love
### **Applies To**
  - *.md
  - *.txt

## Team Blame Language

### **Id**
fc-blame-team
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - team.?failed|they.?did.?not|employee.?fault|staff.?problem
  - if.?they.?had|should.?have.?known|did.?not.?tell.?me
### **Message**
Team blame detected. Founder owns all outcomes. Team failure is leadership failure.
### **Fix Action**
Reframe: 'They failed' → 'I failed to hire right/communicate clearly/set up for success'
### **Applies To**
  - *.md
  - *.txt

## Unnecessary Complexity

### **Id**
fc-complexity-love
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - sophisticated|complex|advanced|intricate|comprehensive.?solution
  - multi-?faceted|nuanced.?approach|holistic
### **Message**
Complexity love detected. Simple beats sophisticated. Most startup problems have simple solutions.
### **Fix Action**
Ask: What is the simplest version? Start there. Add complexity only when proven necessary.
### **Applies To**
  - *.md
  - *.txt