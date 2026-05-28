# Ai For Learning - Validations

## AI Without Guardrails

### **Id**
no-ai-guardrails
### **Severity**
critical
### **Type**
conceptual
### **Check**
AI should be constrained to course scope
### **Indicators**
  - AI can discuss any topic
  - No content grounding
  - No escalation path to human
### **Message**
AI tutor lacks proper guardrails.
### **Fix Action**
Implement RAG with course content, add topic boundaries, create human escalation

## No AI Monitoring

### **Id**
no-ai-monitoring
### **Severity**
high
### **Type**
conceptual
### **Check**
AI conversations should be monitored
### **Indicators**
  - No conversation logging
  - No quality review
  - No student feedback mechanism
### **Message**
AI usage not being monitored.
### **Fix Action**
Log conversations, sample and review regularly, add student report mechanism

## No AI Cost Controls

### **Id**
no-ai-cost-controls
### **Severity**
medium
### **Type**
conceptual
### **Check**
AI costs should be controlled
### **Indicators**
  - No usage limits
  - No spend monitoring
  - No model optimization
### **Message**
AI costs not controlled.
### **Fix Action**
Implement rate limiting, usage monitoring, and budget alerts

## No AI Usage Policy

### **Id**
no-ai-policy
### **Severity**
medium
### **Type**
conceptual
### **Check**
Should have clear AI usage policy
### **Indicators**
  - No policy on AI for assessments
  - Students unclear on allowed use
  - No AI literacy training
### **Message**
Missing clear AI usage policy for students.
### **Fix Action**
Create and communicate clear policy on AI use in learning and assessments

## AI Without Human Fallback

### **Id**
ai-only-no-human
### **Severity**
high
### **Type**
conceptual
### **Check**
Should have human support alongside AI
### **Indicators**
  - No way to reach human
  - AI handles everything
  - No escalation for complex issues
### **Message**
No human fallback for AI support.
### **Fix Action**
Create clear path to human support when AI can't help