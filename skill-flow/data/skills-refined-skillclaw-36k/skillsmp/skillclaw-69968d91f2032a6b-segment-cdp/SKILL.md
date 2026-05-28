---
name: segment-cdp
description: Use this skill when implementing best practices for the Segment Customer Data Platform, including tracking strategies, identity resolution, and data governance.
---

# Segment CDP

## Patterns

### Analytics.js Browser Integration

Implement client-side tracking with Analytics.js. Use track, identify, page, and group calls. An anonymous ID persists until identify merges with the user.

### Server-Side Tracking with Node.js

Utilize high-performance server-side tracking using `@segment/analytics-node`. This method is non-blocking with internal batching, making it essential for backend events, webhooks, and handling sensitive data.

### Tracking Plan Design

Design event schemas using the Object + Action naming convention. Define required properties, types, and validation rules. Connect to Protocols for enforcement.

## Anti-Patterns

### ❌ Dynamic Event Names

### ❌ Tracking Properties as Events

### ❌ Missing Identify Before Track

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Issue | medium | See docs |
| Issue | high | See docs |
| Issue | medium | See docs |
| Issue | high | See docs |
| Issue | low | See docs |
| Issue | medium | See docs |
| Issue | medium | See docs |
| Issue | high | See docs |