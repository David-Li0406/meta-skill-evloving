# Yc Playbook - Validations

## No Metrics in Pitch

### **Id**
yc-no-metrics
### **Severity**
error
### **Type**
regex
### **Pattern**
  - (?i)(pitch|deck|overview|README)(?!.*\d+%|.*\$\d+|.*\d+\s*users|.*\d+\s*customers)
### **Message**
Pitch lacks quantitative metrics. Add growth rate, revenue, or user numbers.
### **Fix Action**
Add: 'Growing 20% MoM' or '$50K MRR' or '10K active users'
### **Applies To**
  - **/pitch.md
  - **/PITCH.md
  - **/deck.md
  - **/README.md

## Unclear Problem Statement

### **Id**
yc-vague-problem
### **Severity**
error
### **Type**
regex
### **Pattern**
  - (?i)problem:?\s*(people|users|companies)\s+(need|want|struggle)(?!.*specific|.*\$\d+|.*hours?|.*\d+%)
### **Message**
Problem statement too vague. Quantify pain: time lost, money wasted, frequency.
### **Fix Action**
Add: 'Companies waste $50K/year on X' or 'Users spend 5 hours/week doing Y'
### **Applies To**
  - **/*.md

## Feature-Focused Instead of Outcome

### **Id**
yc-feature-focused-pitch
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?i)we (build|built|offer|provide|have)\s+a\s+(tool|platform|app|software)\s+that\s+(has|includes|features)
### **Message**
Pitch focuses on features, not outcomes. Lead with customer benefit.
### **Fix Action**
Change to: 'We help X achieve Y by Z' instead of 'We built a tool that...'
### **Applies To**
  - **/pitch.md
  - **/PITCH.md
  - **/README.md

## No Defensibility Discussion

### **Id**
yc-no-moat
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?i)(competitive|moat|advantage|defensible)(?!.*network\s+effect|.*data|.*brand|.*switching\s+cost|.*regulation)
### **Message**
Missing moat/defensibility explanation. Explain sustainable competitive advantage.
### **Fix Action**
Add section on: network effects, proprietary data, brand, switching costs, or regulation
### **Applies To**
  - **/*.md

## Unclear Market Size

### **Id**
yc-unclear-market-size
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?i)market(?!.*\$\d+[BMK]|.*billion|.*million)
### **Message**
Market size not quantified. Estimate TAM/SAM/SOM with dollar amounts.
### **Fix Action**
Add: 'TAM: $5B, SAM: $500M, SOM: $50M in year 3'
### **Applies To**
  - **/*.md

## No Traction Mentioned

### **Id**
yc-no-traction
### **Severity**
error
### **Type**
regex
### **Pattern**
  - (?i)(progress|traction|status)(?!.*launched|.*revenue|.*users?|.*customers?|.*pilot)
### **Message**
No traction/progress mentioned. Add what you've achieved so far.
### **Fix Action**
Add: 'Launched 2 months ago, $10K MRR, 500 users, 3 paying customers'
### **Applies To**
  - **/pitch.md
  - **/PITCH.md

## Team Without Domain Expertise

### **Id**
yc-team-no-expertise
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?i)(team|founder)(?!.*experience|.*background|.*previous|.*built|.*worked at)
### **Message**
Team section lacks domain expertise or relevant background.
### **Fix Action**
Add: 'Founder was head of X at Y' or 'Built similar product at Z'
### **Applies To**
  - **/*.md

## Unclear Business Model

### **Id**
yc-no-business-model
### **Severity**
error
### **Type**
regex
### **Pattern**
  - (?i)business\s+model(?!.*\$/.*month|.*subscription|.*transaction|.*commission|.*license)
### **Message**
Business model not clearly defined. Specify pricing and revenue model.
### **Fix Action**
Add: '$99/month subscription' or '2% transaction fee' or '$5K annual license'
### **Applies To**
  - **/*.md

## Overly Long Explanation

### **Id**
yc-long-explanation
### **Severity**
info
### **Type**
regex
### **Pattern**
  - (?i)^.{500,}$
### **Message**
Explanation exceeds 500 chars. YC says: 'Explain in one clear sentence.'
### **Fix Action**
Simplify: What do you do, for whom, and what's the result? One sentence.
### **Applies To**
  - **/pitch.md
  - **/PITCH.md

## No Clear Ask

### **Id**
yc-no-ask
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?i)(fundraising|raising|seeking)(?!.*\$\d+)
### **Message**
Fundraising mention without clear amount. Specify what you're raising.
### **Fix Action**
Add: 'Raising $500K seed round' or 'Seeking $2M Series A'
### **Applies To**
  - **/*.md

## Buzzword-Heavy Pitch

### **Id**
yc-buzzword-heavy
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?i)(synergy|disrupt|revolutionary|paradigm|cutting-edge|innovative|game-changing)
### **Message**
Buzzwords detected. YC prefers clear, direct language about what you do.
### **Fix Action**
Replace buzzwords with concrete descriptions: 'We reduce X by 50%'
### **Applies To**
  - **/*.md

## Missing Timeline/Roadmap

### **Id**
yc-no-timeline
### **Severity**
info
### **Type**
regex
### **Pattern**
  - (?i)(roadmap|timeline|milestones?)(?!.*month|.*quarter|.*\d{4}|.*Q[1-4])
### **Message**
Timeline mentioned but not specific. Add dates or timeframes.
### **Fix Action**
Add: 'Q1 2024: Launch MVP, Q2: First 100 customers, Q3: Break even'
### **Applies To**
  - **/*.md