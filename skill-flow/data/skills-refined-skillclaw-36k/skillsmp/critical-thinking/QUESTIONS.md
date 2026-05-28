# Critical Questions by Domain

Targeted questions for evaluating technical decisions across different domains.

---

## Architecture & System Design

### Problem Definition
| Question | Red Flag If... |
|----------|----------------|
| What specific problem are we solving? | Vague or shifting definition |
| Who are the users and what do they need? | Unknown or assumed |
| What are the success criteria? | Not measurable |
| What happens if we do nothing? | No clear cost of inaction |

### Solution Evaluation
| Question | Red Flag If... |
|----------|----------------|
| What alternatives did we consider? | None, or dismissed without analysis |
| Why is this better than alternatives? | "It's what we know" or "everyone uses it" |
| What are we optimizing for? | Everything (can't optimize for all) |
| What are we explicitly NOT optimizing for? | Nothing listed (hidden trade-offs) |

### Complexity Assessment
| Question | Red Flag If... |
|----------|----------------|
| Could a simpler solution work? | Dismissed without evidence |
| What's the minimum viable approach? | Starts at full complexity |
| How many moving parts are there? | Can't list them |
| What's the learning curve? | "It's just like X" (usually isn't) |

### Evolution & Maintenance
| Question | Red Flag If... |
|----------|----------------|
| How will this change in 2 years? | "It won't need to change" |
| What happens when requirements change? | Requires full rewrite |
| Who will maintain this? | "We'll figure it out" |
| How do we migrate away if needed? | No exit strategy |

---

## Performance & Scalability

### Baseline Questions
| Question | Red Flag If... |
|----------|----------------|
| What's the current performance? | Unknown or unmeasured |
| What's the target performance? | Arbitrary or aspirational |
| How did we arrive at these numbers? | "Industry standard" or guessed |
| What's the bottleneck? | Unknown or assumed |

### Load & Capacity
| Question | Red Flag If... |
|----------|----------------|
| What's the expected load? | Round numbers (probably guessed) |
| What's the growth trajectory? | Hockey stick without evidence |
| What happens at 2x, 5x, 10x load? | Untested |
| Where will it break first? | Unknown |

### Measurement & Evidence
| Question | Red Flag If... |
|----------|----------------|
| How was this benchmarked? | Vendor benchmarks only |
| What's the test methodology? | Synthetic/unrealistic |
| What are the test conditions? | Best case scenario |
| Who else runs this at scale? | Can't name specific examples |

### Optimization Validity
| Question | Red Flag If... |
|----------|----------------|
| Is this premature optimization? | "We might need it" |
| What's the actual impact? | Theoretical only |
| What's the cost of this optimization? | Not considered |
| Is the bottleneck actually here? | Assumed, not measured |

---

## Security

### Threat Model
| Question | Red Flag If... |
|----------|----------------|
| What's the threat model? | None defined |
| Who are the adversaries? | "Generic hackers" |
| What are we protecting? | Everything (means nothing) |
| What's the value of the assets? | Unknown |

### Access & Authentication
| Question | Red Flag If... |
|----------|----------------|
| Who has access to what? | Everyone has admin |
| How is authentication handled? | Custom/homegrown |
| How are credentials stored? | In code or env vars |
| What happens when credentials are compromised? | No rotation plan |

### Data Protection
| Question | Red Flag If... |
|----------|----------------|
| What data is sensitive? | Unknown classification |
| How is data encrypted? | In transit only, or not at all |
| Who can access production data? | Too many people |
| How do we detect data breaches? | We don't |

### Incident Response
| Question | Red Flag If... |
|----------|----------------|
| How do we detect attacks? | No monitoring |
| What's the response plan? | None exists |
| How do we recover? | Never tested |
| How do we learn from incidents? | No post-mortem process |

---

## Database & Data Design

### Schema Design
| Question | Red Flag If... |
|----------|----------------|
| What queries will this support? | Unknown or all of them |
| How will data grow over time? | Unbounded growth assumed okay |
| What are the access patterns? | Not analyzed |
| What indexes are needed? | Added after performance issues |

### Consistency & Integrity
| Question | Red Flag If... |
|----------|----------------|
| What's the consistency model? | Unknown or assumed |
| How do we handle concurrent writes? | "It's not a problem" |
| What happens during failures? | Data loss acceptable |
| How do we detect corruption? | We don't |

### Migration & Evolution
| Question | Red Flag If... |
|----------|----------------|
| How do we migrate schema? | Downtime required |
| What's the rollback plan? | None |
| How do we backfill data? | Manual process |
| What happens to old data? | Kept forever |

---

## Dependencies & Third-Party Services

### Evaluation
| Question | Red Flag If... |
|----------|----------------|
| What problem does this solve? | "It's popular" |
| What's the maintenance status? | Last update 2+ years ago |
| Who maintains it? | Single maintainer |
| What's the license? | Unknown or GPL in commercial |

### Risk Assessment
| Question | Red Flag If... |
|----------|----------------|
| What happens if this goes away? | No alternative identified |
| Can we replace this later? | Deep integration required |
| What's the vendor lock-in? | High switching costs |
| Who else uses this at scale? | No production references |

### Integration
| Question | Red Flag If... |
|----------|----------------|
| What's the failure mode? | Unknown |
| How do we handle outages? | No fallback |
| What's the SLA? | None or "best effort" |
| How do we monitor this? | We don't |

---

## API Design

### Contract
| Question | Red Flag If... |
|----------|----------------|
| What's the versioning strategy? | None |
| How do we handle breaking changes? | Yolo |
| What's the error contract? | Inconsistent |
| How is the API documented? | "The code is the docs" |

### Reliability
| Question | Red Flag If... |
|----------|----------------|
| What's the timeout strategy? | None or infinite |
| How do we handle rate limiting? | We don't |
| What's the retry strategy? | Infinite retries |
| How do we handle partial failures? | All or nothing |

---

## Testing Strategy

### Coverage
| Question | Red Flag If... |
|----------|----------------|
| What's the testing strategy? | "We'll add tests later" |
| What's NOT tested? | Unknown |
| How do we test failure scenarios? | We don't |
| How do we test integration points? | Mocks only |

### Confidence
| Question | Red Flag If... |
|----------|----------------|
| What does a passing test suite tell us? | "It works" (too vague) |
| What can still break despite tests? | Unknown |
| How long do tests take to run? | Hours (won't be run often) |
| How flaky are the tests? | "Sometimes they fail" |

---

## Deployment & Operations

### Release Strategy
| Question | Red Flag If... |
|----------|----------------|
| How do we deploy? | Manual process |
| What's the rollback plan? | Restore from backup |
| How long does deployment take? | Hours |
| What's the blast radius? | All users |

### Monitoring & Observability
| Question | Red Flag If... |
|----------|----------------|
| How do we know it's working? | Users tell us |
| What alerts are in place? | None |
| How do we debug production issues? | SSH into servers |
| What's the on-call process? | No on-call |

### Incident Management
| Question | Red Flag If... |
|----------|----------------|
| How do we detect incidents? | Customer complaints |
| What's the escalation path? | Figure it out |
| How do we communicate during incidents? | Ad hoc |
| How do we learn from incidents? | We don't |

---

## Quick Reference: Universal Questions

These apply to almost any technical decision:

1. **What problem are we actually solving?**
2. **What are the alternatives?**
3. **What are the trade-offs?**
4. **What evidence supports this?**
5. **What happens when it fails?**
6. **How will we know it's working?**
7. **What's the maintenance burden?**
8. **Can we reverse this decision?**
9. **Who else has done this successfully?**
10. **What's the simplest approach that could work?**

---

## Question Intensity Guide

| Risk Level | Question Depth | When |
|------------|----------------|------|
| **High** | All questions, verification required | Core architecture, security, data |
| **Medium** | Key questions, spot verification | Features, integrations |
| **Low** | Quick sanity check | Config, cosmetic changes |

> Rule of thumb: Question intensity should match decision reversibility and impact.
