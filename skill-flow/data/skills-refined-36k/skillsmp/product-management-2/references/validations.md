# Product Management - Validations

## Missing User Story Format

### **Id**
pm-no-user-story
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ##?\s*Feature:\s*\w+(?!.{0,500}\b(As a|As an)\b)
  - ##?\s*Story:(?!.{0,200}\b(As a|As an)\b.{0,100}\bI want\b)
### **Message**
Feature described without user story format. User stories connect features to user needs.
### **Fix Action**
Use format: 'As a [user type], I want [goal] so that [benefit]'
### **Applies To**
  - *.md
  - *.txt

## Missing Acceptance Criteria

### **Id**
pm-no-acceptance-criteria
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ##?\s*(Story|Feature|Epic):\s*\w+(?!.{0,800}\b(Acceptance Criteria|AC:|Given|When|Then)\b)
### **Message**
Story lacks acceptance criteria. AC defines 'done' and prevents scope creep.
### **Fix Action**
Add acceptance criteria section with Given-When-Then scenarios or checklist of requirements
### **Applies To**
  - *.md
  - *.txt

## Missing Priority or Impact

### **Id**
pm-no-priority
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ##?\s*(Story|Feature|Epic)(?!.{0,500}\b(Priority|Impact|MoSCoW|Critical|High|Medium|Low)\b)
### **Message**
No priority level assigned. Prioritization is essential for roadmap planning.
### **Fix Action**
Add priority (Critical/High/Medium/Low) or impact/effort rating
### **Applies To**
  - *.md
  - *.txt

## Scope Creep Language Detected

### **Id**
pm-scope-creep-language
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \b(also|and also|while we're at it|might as well|plus)\b
  - \b(just add|simply|easy to|quick win)\b.{0,50}\b(feature|change)\b
### **Message**
Language suggesting scope creep. Adding features mid-sprint derails planning.
### **Fix Action**
Create separate story for additional scope. Protect current sprint commitment.
### **Applies To**
  - *.md
  - *.txt

## Missing Success Metrics

### **Id**
pm-no-success-metrics
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ##?\s*(Epic|Feature|Initiative)(?!.{0,800}\b(metric|KPI|measure|goal|target|success)\b)
### **Message**
Feature/epic without success metrics. Can't validate if solution solves the problem.
### **Fix Action**
Define measurable success criteria: conversion rate +X%, reduction in support tickets, etc.
### **Applies To**
  - *.md
  - *.txt

## Solution Before Problem Statement

### **Id**
pm-solution-before-problem
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ##?\s*(Feature|Story).{0,100}\b(build|create|implement|add)\b(?!.{0,500}\b(Problem|Why|User need|Pain point)\b)
### **Message**
Solution described before problem. Start with user problem, not implementation.
### **Fix Action**
Add 'Problem' or 'User Need' section before describing solution
### **Applies To**
  - *.md
  - *.txt

## Missing Edge Cases

### **Id**
pm-no-edge-cases
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ##?\s*Acceptance Criteria(?!.{0,500}\b(edge case|error|failure|empty|null|zero|max|invalid)\b)
### **Message**
Acceptance criteria don't mention edge cases. Most bugs come from edge cases.
### **Fix Action**
Add edge cases: empty state, error handling, max limits, invalid input, network failure
### **Applies To**
  - *.md
  - *.txt

## Vague Requirements Language

### **Id**
pm-vague-requirements
### **Severity**
error
### **Type**
regex
### **Pattern**
  - \b(user-friendly|intuitive|easy to use|simple|clean|modern)\b
  - \b(fast|quick|responsive|performant)\b(?!.{0,100}\d+\s*(ms|sec|MB))
### **Message**
Vague, subjective requirements. Subjective terms are not testable.
### **Fix Action**
Use specific, measurable criteria: '<200ms load time', 'accessible (WCAG 2.1 AA)', '3 clicks max'
### **Applies To**
  - *.md
  - *.txt

## Missing User Persona

### **Id**
pm-no-personas
### **Severity**
info
### **Type**
regex
### **Pattern**
  - \b(user|customer)\b(?!.{0,300}\b(persona|segment|type|role|admin|creator|viewer)\b)
### **Message**
Generic 'user' without persona specificity. Different users have different needs.
### **Fix Action**
Specify user persona: 'admin user', 'free tier user', 'power user', etc.
### **Applies To**
  - *.md
  - *.txt

## Missing Dependencies

### **Id**
pm-no-dependencies
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ##?\s*(Epic|Feature|Story)(?!.{0,800}\b(depends on|blocked by|requires|prerequisite|dependency)\b)
### **Message**
No dependencies mentioned. Untracked dependencies cause delays.
### **Fix Action**
Document dependencies: API endpoints, other features, infrastructure, third-party services
### **Applies To**
  - *.md
  - *.txt

## Missing Risk Assessment

### **Id**
pm-no-risks
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ##?\s*(Epic|Feature|Initiative)(?!.{0,1000}\b(risk|assumption|uncertainty|unknown|question)\b)
### **Message**
No risks or assumptions documented. Unstated assumptions become costly surprises.
### **Fix Action**
Add 'Risks & Assumptions' section: technical unknowns, user behavior assumptions, dependencies
### **Applies To**
  - *.md
  - *.txt

## Missing Alternative Solutions

### **Id**
pm-no-alternatives
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ##?\s*Solution(?!.{0,500}\b(alternative|option|considered|instead|vs)\b)
### **Message**
Only one solution considered. Best solutions emerge from comparing alternatives.
### **Fix Action**
Document 2-3 alternatives considered and why current approach was chosen
### **Applies To**
  - *.md
  - *.txt

## Waterfall Process Language

### **Id**
pm-waterfall-language
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \b(complete|finish|finalize)\b.{0,50}\b(before|then)\b
  - \b(Phase [123]|Stage [123])\b.{0,100}\b(must be done|complete before)\b
### **Message**
Sequential waterfall language detected. Agile favors iterative delivery with feedback loops.
### **Fix Action**
Break into iterative increments: MVP → iterate based on feedback → expand
### **Applies To**
  - *.md
  - *.txt