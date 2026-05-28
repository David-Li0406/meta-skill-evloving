# Early Stage Hustle - Validations

## Premature Scaling

### **Id**
hustle-premature-scale
### **Severity**
error
### **Type**
regex
### **Pattern**
  - hire|hiring|team|staff|headcount|scale.?up|expand.?team
### **Message**
Hiring/scaling before PMF. Adding people to an unproven model = burning money faster. Stay lean.
### **Fix Action**
Validate first: Get to product-market fit with founders only. Hire only when repeatably acquiring customers.
### **Applies To**
  - *.md
  - *.txt
  - README*

## Lack of Focus

### **Id**
hustle-no-focus
### **Severity**
error
### **Type**
regex
### **Pattern**
  - and|also|plus|additionally|as.?well.?as|in.?addition
### **Message**
Doing too many things. Early stage = brutal focus. One target customer, one core problem, one channel.
### **Fix Action**
Cut everything except the ONE thing that could work. Do that intensely. Add back later.
### **Applies To**
  - *.md
  - *.txt

## Perfect Over Done

### **Id**
hustle-perfect-not-done
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - polish|perfect|refine|improve|optimize|enhance
### **Message**
Optimizing before shipping. Perfect is the enemy of shipped. Early stage is about learning, not perfection.
### **Fix Action**
Ship now, iterate fast. Get it in users' hands. Real feedback > theoretical perfection.
### **Applies To**
  - *.md
  - *.txt

## No Resource Constraints

### **Id**
hustle-no-constraints
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - need|require|should.?have|want|would.?like
### **Message**
No constraints mentioned. Constraints breed creativity. What can you do with time/money you have right now?
### **Fix Action**
Work within limits: What can you build in 1 week? What costs $0? Resourcefulness > resources.
### **Applies To**
  - *.md
  - *.txt

## Process Over Results

### **Id**
hustle-process-over-results
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - process|framework|methodology|system|structure|organization
### **Message**
Building process before traction. Startups die from lack of customers, not lack of process. Get customers first.
### **Fix Action**
Focus on outcomes: revenue, users, retention. Process comes later when you're repeating what works.
### **Applies To**
  - *.md
  - *.txt

## Long-Term Roadmap

### **Id**
hustle-long-roadmap
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - quarter|Q1|Q2|Q3|Q4|6.?months|year|annual|long.?term
### **Message**
Long-term planning before validation. Early stage = 2-week sprints. Plan further once you find traction.
### **Fix Action**
Think in weeks: What ships this week? What did we learn? What's next week? Iterate fast.
### **Applies To**
  - *.md
  - *.txt

## Delegating Core Work

### **Id**
hustle-delegate-core
### **Severity**
error
### **Type**
regex
### **Pattern**
  - outsource|contractor|freelance|agency|hire.?someone
### **Message**
Outsourcing core work early. Founders must do the hard stuff first. You can't delegate learning.
### **Fix Action**
Do it yourself first: sales, customer support, product. Learn deeply. Then maybe delegate later.
### **Applies To**
  - *.md
  - *.txt

## Premature Automation

### **Id**
hustle-automation-too-early
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - automate|automation|tool|software|platform|build.?system
### **Message**
Automating before knowing what works. Do things manually first. Automate only what's proven and repetitive.
### **Fix Action**
Manual first: Talk to every customer, send personal emails, do things that don't scale. Then automate.
### **Applies To**
  - *.md
  - *.txt

## Fundraising Before Validation

### **Id**
hustle-raise-before-validation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - raise|funding|investment|investors|seed|series
### **Message**
Fundraising focus before product validation. Money doesn't solve 'no one wants this' problem. Validate first.
### **Fix Action**
Bootstrap to validation: Get to $10K MRR or strong usage. Then raise from position of strength.
### **Applies To**
  - *.md
  - *.txt

## Over-Engineering

### **Id**
hustle-over-engineering
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - architecture|infrastructure|scalable|enterprise|production.?ready|robust
### **Message**
Building for scale before finding users. You don't need to serve millions when you have zero. Ship ugly, iterate.
### **Fix Action**
Build for 10 users first. No-code, duct tape, manual work. Over-engineer only when you have the problem.
### **Applies To**
  - *.md
  - *.txt

## Not Talking to Customers

### **Id**
hustle-no-customer-contact
### **Severity**
error
### **Type**
regex
### **Pattern**
  - building|developing|creating|coding|feature
### **Message**
Building without customer contact. You should talk to users every single day. No exceptions.
### **Fix Action**
Daily customer conversations: sales calls, support, user interviews. Stay connected to their reality.
### **Applies To**
  - *.md
  - *.txt

## Waiting for Perfect Conditions

### **Id**
hustle-waiting-perfect-time
### **Severity**
error
### **Type**
regex
### **Pattern**
  - when|once|after|until|before.?we|need.?to.?wait
### **Message**
Waiting for perfect conditions. There is no perfect time. Start messy, figure it out as you go.
### **Fix Action**
Start now with what you have: imperfect product, no funding, wrong skills. Resourcefulness beats resources.
### **Applies To**
  - *.md
  - *.txt