# Founder Operating System - Validations

## Missing Clear Priorities

### **Id**
fos-no-priorities
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - priority|priorities|important|critical|must.?do
### **Message**
Priorities mentioned but often everything is priority 1. If everything is important, nothing is.
### **Fix Action**
Force rank: What is THE ONE thing this week? What are you explicitly NOT doing?
### **Applies To**
  - *.md
  - *.txt

## Meeting-Heavy Process

### **Id**
fos-meeting-overload
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - meeting|standup|sync|check-?in|huddle|all-?hands
### **Message**
Meeting-centric language detected. Meetings are interruptions. Default to async.
### **Fix Action**
Ask: Can this be a Slack message? A Loom? A doc? Reserve meetings for decisions and debates.
### **Applies To**
  - *.md
  - *.txt

## Unclear Ownership

### **Id**
fos-unclear-ownership
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - we.?will|team.?will|someone|anyone|everybody
### **Message**
Unclear ownership detected. 'We will' means nobody will. Every task needs a single owner.
### **Fix Action**
Assign one DRI (Directly Responsible Individual) to each item with deadline
### **Applies To**
  - *.md
  - *.txt

## Task Without Deadline

### **Id**
fos-no-deadline
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - eventually|soon|when.?possible|asap|later|sometime
### **Message**
Vague timeline detected. Tasks without deadlines do not get done.
### **Fix Action**
Add specific date: 'soon' → 'by Friday Dec 20' or 'not this quarter'
### **Applies To**
  - *.md
  - *.txt

## Process Over Outcome

### **Id**
fos-process-heavy
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - process|procedure|policy|workflow|framework|methodology
### **Message**
Process-heavy language detected. Process is overhead. Minimize until absolutely necessary.
### **Fix Action**
Ask: What outcome are we trying to achieve? What is the minimum process to get there?
### **Applies To**
  - *.md
  - *.txt

## Goals Without Metrics

### **Id**
fos-no-metrics
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - improve|better|increase|grow|enhance|optimize
### **Message**
Improvement goal without metric. How will you know if you improved?
### **Fix Action**
Add measurement: 'improve retention' → 'increase 30-day retention from 40% to 50%'
### **Applies To**
  - *.md
  - *.txt

## Scope Creep Language

### **Id**
fos-scope-creep
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - also|plus|additionally|and.?also|while.?we.?are|might.?as.?well
### **Message**
Scope creep language detected. Adding scope is easy. Cutting is leadership.
### **Fix Action**
For every add, identify a cut. Maintain focus. Scope is a zero-sum game.
### **Applies To**
  - *.md
  - *.txt

## Missing Review Cadence

### **Id**
fos-no-review-cadence
### **Severity**
info
### **Type**
regex
### **Pattern**
  - goal|objective|target|okr|kpi
### **Message**
Goals without review cadence. Unreviewed goals are forgotten goals.
### **Fix Action**
Add review schedule: weekly metrics, monthly retrospective, quarterly planning
### **Applies To**
  - *.md
  - *.txt

## Deferred Decision

### **Id**
fos-decision-debt
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - TBD|to.?be.?determined|decide.?later|figure.?out|revisit
### **Message**
Deferred decision detected. Decision debt compounds. Decide now or schedule the decision.
### **Fix Action**
Either decide now with available info, or set specific date and owner for decision
### **Applies To**
  - *.md
  - *.txt

## Plan Without Constraints

### **Id**
fos-no-constraints
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - plan|roadmap|strategy|initiative
### **Message**
Plan without explicit constraints. Every plan needs time, budget, and scope limits.
### **Fix Action**
Add constraints: deadline, budget, team size. Plans without limits expand forever.
### **Applies To**
  - *.md
  - *.txt

## Success Theater Language

### **Id**
fos-success-theater
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - great.?progress|going.?well|on.?track|everything.?fine|no.?issues
### **Message**
Success theater language detected. Surface problems early. Hidden problems grow.
### **Fix Action**
Add specific evidence: 'on track' → 'X of Y complete, Z risk identified, mitigating by...'
### **Applies To**
  - *.md
  - *.txt

## Over-Scheduled Calendar

### **Id**
fos-calendar-tetris
### **Severity**
info
### **Type**
regex
### **Pattern**
  - busy|packed|back.?to.?back|no.?time|overloaded|slammed
### **Message**
Calendar overload detected. Busy is not productive. Protect time for deep work.
### **Fix Action**
Block 4+ hours daily for focused work. Batch meetings. Say no to most.
### **Applies To**
  - *.md
  - *.txt