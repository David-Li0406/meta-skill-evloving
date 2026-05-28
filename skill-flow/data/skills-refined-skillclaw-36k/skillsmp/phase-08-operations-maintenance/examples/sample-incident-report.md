# Example: ShopEase Production Incident Report

**Document ID:** P8-INC-001  
**Incident ID:** INC-20260315-001  
**Status:** Closed  
**Author:** Jamie Rodriguez, Incident Commander  

---

## 1. Incident Summary

| Field | Value |
|-------|-------|
| **Title** | Payment Service Outage |
| **Severity** | SEV1 |
| **Service(s) Affected** | Payment Service, Checkout |
| **Duration** | 47 minutes |
| **Impact** | 2,847 failed checkout attempts |
| **Root Cause** | Database connection pool exhaustion |

---

## 2. Timeline

| Time (UTC) | Event |
|------------|-------|
| 14:23 | First payment failures detected by monitoring |
| 14:25 | PagerDuty alert triggered, on-call paged |
| 14:28 | On-call acknowledged, began investigation |
| 14:35 | Identified high DB connection count |
| 14:42 | Root cause identified: connection leak in new code |
| 14:48 | Rolled back to previous version |
| 14:55 | Service restored, monitoring normal |
| 15:10 | Incident declared resolved |

**Total Duration:** 47 minutes  
**Time to Detect (TTD):** 2 minutes  
**Time to Resolve (TTR):** 32 minutes

---

## 3. Root Cause Analysis

### What Happened
A code change deployed at 13:45 UTC introduced a connection leak in the payment service. Database connections were not being properly closed after transactions, causing the connection pool to exhaust over ~40 minutes.

### Why It Happened
The new payment retry logic opened a new database connection for each retry attempt but failed to close connections on the retry path. Code review missed this issue because the happy path correctly closed connections.

### Five Whys
1. **Why did payments fail?** Database connections exhausted
2. **Why were connections exhausted?** Connections not being closed
3. **Why weren't they closed?** Bug in retry logic
4. **Why wasn't the bug caught?** Tests didn't cover retry path
5. **Why no retry path tests?** Insufficient test coverage requirements

---

## 4. Action Items

| ID | Action | Owner | Due Date | Status |
|----|--------|-------|----------|--------|
| AI-001 | Add connection pool monitoring alert | SRE | 2026-03-17 |  Done |
| AI-002 | Fix connection leak in payment service | Dev | 2026-03-18 |  Done |
| AI-003 | Add integration tests for retry paths | QA | 2026-03-22 |  Done |
| AI-004 | Update code review checklist | Tech Lead | 2026-03-25 |  Done |

---

**Incident Closed:** 2026-03-16

---

**Document End**

---

**Version 1.0.0 | OCTALUME Enterprise Lifecycle Framework**
