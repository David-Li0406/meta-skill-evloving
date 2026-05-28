# Example: Incident Communication

## 📝 Prompt

```
Write incident communication for a 2-hour service outage.

Context:
- E-commerce checkout service was down
- Occurred during business hours (2pm-4pm EST)
- Affected 15,000 customers
- Root cause: Database failover issue
- Resolution: Manual intervention by engineering
- Revenue impact: ~$50K in lost sales

Audience:
- Internal: All employees
- External: Affected customers

Tone: Professional, transparent, apologetic

Include:
- Timeline of events
- What happened and why
- Impact assessment
- What we're doing to prevent recurrence
- Customer compensation (if any)
```

## ✅ Example Output

---

# Incident Report: Checkout Service Outage
**Date**: January 20, 2026  
**Duration**: 2 hours (2:00 PM - 4:00 PM EST)  
**Status**: Resolved  
**Severity**: SEV-1 (Critical)

---

## Executive Summary

On January 20, 2026, our checkout service experienced a complete outage from 2:00 PM to 4:00 PM EST (2 hours). During this time, customers were unable to complete purchases on our platform. We sincerely apologize for this disruption and the inconvenience it caused.

**Impact:**
- ~15,000 customers affected
- 100% of checkout attempts failed
- Estimated $50,000 in lost revenue
- Browse and search functionality remained operational

**Root Cause:** Database failover mechanism failed during routine maintenance, causing the primary database to become unavailable without automatic promotion of the replica.

**Resolution:** Engineering team performed manual failover and validated data consistency.

**Prevention:** Implementing automated health checks and improving failover automation.

---

## Detailed Timeline

All times in EST.

| Time | Event |
|------|-------|
| 1:45 PM | Scheduled maintenance window begins |
| 2:00 PM | Primary database goes offline as planned |
| 2:01 PM | **Automatic failover fails** - Replica not promoted |
| 2:02 PM | First customer complaints received |
| 2:03 PM | PagerDuty alerts fire - SEV-1 incident declared |
| 2:05 PM | Incident commander (Jane Smith) assigned |
| 2:08 PM | Engineering team assembled on incident bridge |
| 2:15 PM | Root cause identified: failover automation bug |
| 2:20 PM | Decision made to perform manual failover |
| 2:35 PM | Manual failover completed |
| 2:40 PM | Health checks passing - service restored |
| 2:45 PM | Monitoring for stability |
| 3:00 PM | Traffic returning to normal levels |
| 4:00 PM | Incident closed - all metrics nominal |

---

## What Happened

### Background
During our scheduled maintenance window, we initiated a routine database upgrade that required a brief period where the primary database would be offline. Our system is designed to automatically promote a read replica to become the new primary, ensuring minimal downtime.

### The Problem
When the primary database went offline, the automated failover mechanism did not trigger as expected. A bug in our failover automation (introduced in last week's deployment) caused the health check to incorrectly report the replica as unhealthy, preventing automatic promotion.

### Detection & Response
- **2:02 PM**: Customer support received first reports of checkout failures
- **2:03 PM**: Automated monitoring detected the issue and paged the on-call engineer
- **2:05 PM**: SEV-1 incident declared, incident commander assigned
- **2:08 PM**: Cross-functional incident response team assembled

### Resolution
After identifying the issue with automated failover, the engineering team made the decision to perform a manual failover. This involved:
1. Validating replica database health
2. Manually promoting replica to primary
3. Updating application connection strings
4. Verifying data consistency
5. Gradually restoring traffic

By 2:40 PM, the service was fully restored and operating normally.

---

## Impact Analysis

### Customer Impact

**Affected Customers:** ~15,000 unique users attempted to check out during the outage

**User Experience:**
- Checkout button appeared to be loading indefinitely
- Some users saw error message: "We're experiencing technical difficulties"
- Shopping cart data was preserved
- No customer data was lost

**Revenue Impact:**
- Estimated $50,000 in lost sales
- 1,200 abandoned carts during outage
- Average cart value: $42

### System Impact

**Services Affected:**
- ❌ Checkout service (100% failure rate)
- ❌ Order placement
- ❌ Payment processing

**Services Unaffected:**
- ✅ Product browsing
- ✅ Search functionality
- ✅ User account management
- ✅ Customer support portal

---

## Root Cause Analysis

### Primary Cause
Bug in database failover automation script (deployed Jan 13, 2026) caused health check to incorrectly evaluate replica status.

**Specific Issue:**
```python
# Bug in health_check.py
def check_replica_health(replica):
    # BUG: Using wrong timeout value
    if replica.lag > 100:  # Should be 1000ms
        return False
```

The health check was using an overly strict threshold (100ms vs 1000ms), causing the replica to be marked as unhealthy even though it was fully operational with acceptable replication lag.

### Contributing Factors

1. **Insufficient Testing**
   - Failover automation was tested in staging but not under realistic load
   - No chaos engineering tests for this scenario

2. **Lack of Alerting**
   - No proactive alert for "automatic failover disabled"
   - Only alerted after service was already down

3. **Manual Process Gap**
   - Manual failover playbook was outdated
   - Team needed to reference documentation during incident

4. **Communication Delay**
   - Customer support wasn't immediately notified
   - Status page update was delayed by 5 minutes

---

## What We're Doing About It

### Immediate Actions (Completed)

✅ **Reverted problematic deployment** (Jan 20, 4:15 PM)
- Rolled back failover automation to previous stable version
- Verified automatic failover working correctly

✅ **Data validation** (Jan 20, 6:00 PM)
- Confirmed zero data loss
- Verified all customer carts preserved

✅ **Customer communication** (Jan 20, 5:00 PM)
- Email sent to affected customers
- Status page updated with full timeline
- Social media responses to inquiries

### Short-term Actions (This Week)

🔄 **Enhanced monitoring** (Jan 22)
- Add alerting for "failover automation disabled"
- Implement canary deployments for critical services
- Add real-time health dashboard for all database replicas

🔄 **Chaos engineering** (Jan 24)
- Scheduled chaos test: database failure scenarios
- Validation of all automated failover paths

🔄 **Updated runbooks** (Jan 23)
- Refresh manual failover documentation
- Add flowchart for incident response
- Conduct table-top exercise with team

### Long-term Improvements (Next 30 Days)

📅 **Architectural improvements** (Feb 15)
- Implement multi-region database clusters
- Add circuit breakers for database connections
- Deploy read-only fallback mode for degraded state

📅 **Process improvements** (Feb 10)
- Mandatory load testing for infrastructure changes
- Enhanced change management for database deployments
- Quarterly disaster recovery drills

📅 **Communication improvements** (Feb 5)
- Automated customer support notifications
- Real-time status page updates
- Pre-drafted incident templates

---

## Customer Compensation

To apologize for this disruption, we are providing:

### For All Affected Customers
- **$10 store credit** (automatically applied within 24 hours)
- Valid for 90 days
- No minimum purchase required

### For Premium Members
- **$25 store credit** + **1 month subscription extension**
- Priority support for 30 days

### For Customers with Abandoned Carts Over $100
- **Additional $15 credit**
- Personal email with direct support contact

**Total Estimated Cost:** ~$180,000 in credits and subscription extensions

---

## Communication Templates

### Internal Email (Sent to All Employees)

```
Subject: [RESOLVED] Incident Report: 2-hour Checkout Outage - Jan 20

Team,

I want to update you on today's service incident.

WHAT HAPPENED:
Between 2-4 PM EST today, our checkout service was completely unavailable 
for 2 hours. Customers could browse products but couldn't complete purchases.

IMPACT:
- 15,000 customers affected
- ~$50K in lost revenue
- No data loss

ROOT CAUSE:
A bug in our database failover automation (deployed last week) prevented 
automatic recovery during routine maintenance. Engineering had to perform 
manual failover.

RESOLUTION:
- Service fully restored at 2:40 PM
- Bug fixed and deployment reverted
- All systems operating normally

WHAT WE'RE DOING:
- Enhanced monitoring and alerting
- Architecture improvements for multi-region failover
- $180K in customer credits as apology

CUSTOMER RESPONSE:
We've proactively communicated with affected customers and are providing 
compensation. Support should expect increased ticket volume this week.

Thank you to the incident response team for their quick work, and to 
customer support for handling this professionally.

Questions? Join tomorrow's all-hands or contact me directly.

- Chris Johnson, CTO
```

---

### External Email (Sent to Affected Customers)

```
Subject: We're Sorry - Here's $10 on Us

Dear [Customer Name],

We owe you an apology.

Today between 2-4 PM ET, you may have tried to check out on our site and 
experienced an error. This was due to a technical issue on our end that 
prevented anyone from completing purchases for about 2 hours.

We know how frustrating this is, especially if you had time set aside 
for shopping. Your cart items are still saved, and we'd love for you 
to give us another chance.

As an apology, we've added $10 credit to your account. It's already 
there - no code needed. Use it on anything, anytime in the next 90 days.

WHAT HAPPENED:
A database issue prevented our checkout from working. We fixed it and 
added safeguards to prevent this from happening again.

YOUR CART:
If you had items in your cart, they're still there waiting for you.
[View Your Cart]

QUESTIONS?
Our support team is standing by if you have any concerns.
[Contact Support]

Again, we're sorry for the inconvenience. We appreciate your patience 
and your business.

- The [Company] Team

P.S. Premium members, check your email for additional compensation.
```

---

### Status Page Update

```
🟢 RESOLVED - Checkout Service Restored

Incident: Checkout Service Unavailable
Status: Resolved
Time: Jan 20, 2:00 PM - 4:00 PM EST
Duration: 2 hours

What happened:
A database failover issue prevented customers from completing purchases.

Resolution:
Engineering performed manual failover. Service fully restored.

Impact:
- Checkout unavailable for 2 hours
- Browsing and search unaffected
- No data loss

Next steps:
- Enhanced monitoring implemented
- Architecture improvements in progress
- Full post-mortem report: [Link]

Affected customers will receive compensation within 24 hours.

Last updated: Jan 20, 4:30 PM EST
```

---

### Social Media Response

**Twitter/X:**
```
We experienced a checkout issue today from 2-4pm ET. It's now resolved. 
We're sorry for the disruption and are compensating affected customers. 
Full details: [link to status page]
```

**Response to customer complaints:**
```
We're so sorry about that! The issue is now fixed. Please DM us your 
email address and we'll make sure you receive the $10 credit we're 
giving to affected customers.
```

---

## Lessons Learned

### What Went Well ✅

1. **Fast incident declaration** - SEV-1 declared within 1 minute of detection
2. **Clear incident command** - Roles and responsibilities well-defined
3. **Cross-functional collaboration** - Engineering, product, support worked together
4. **Transparent communication** - Regular updates to stakeholders
5. **Data integrity maintained** - Zero customer data lost

### What Could Be Better 🔧

1. **Testing gaps** - Failover scenario not adequately tested pre-deployment
2. **Monitoring blind spots** - No alert for "automated failover disabled"
3. **Customer communication delay** - 5 minutes before status page update
4. **Manual intervention required** - Should be fully automated
5. **Documentation** - Runbooks were outdated

### Action Items by Owner

**Engineering (@CTO)**
- [ ] Deploy enhanced monitoring (Jan 22)
- [ ] Conduct chaos test (Jan 24)
- [ ] Multi-region database architecture (Feb 15)

**Product (@VP Product)**
- [ ] Review compensation approach with finance (Jan 21)
- [ ] Customer survey on incident (Jan 25)

**Customer Support (@Support Lead)**
- [ ] Train team on technical incident response (Jan 23)
- [ ] Update support macros for incident scenarios (Jan 22)

**Communications (@Comms Lead)**
- [ ] Create incident communication templates (Jan 24)
- [ ] Improve status page automation (Feb 5)

---

## Questions & Answers

**Q: Will this happen again?**  
A: We've identified and fixed the specific bug that caused this incident. We're also implementing architectural changes to prevent similar issues. No system is perfect, but we're committed to continuous improvement.

**Q: Was any customer data compromised?**  
A: No. This was a service availability issue, not a security breach. All customer data remained secure and no information was lost.

**Q: How can I check if I was affected?**  
A: If you attempted to check out between 2-4 PM EST on Jan 20, you were affected. We've proactively emailed all affected customers.

**Q: When will I receive my credit?**  
A: Credits are being applied automatically within 24 hours. Check your account or email for confirmation.

**Q: Can I trust your site now?**  
A: Yes. This was an isolated incident that we've resolved. We process thousands of successful orders daily and have strong infrastructure in place. We're making it even stronger.

---

## Contact

**For Internal Questions:**
- Incident Commander: jane.smith@company.com
- Engineering: engineering-leads@company.com
- Join #incident-2026-01-20 on Slack

**For Customer Questions:**
- Support: support@company.com
- Status: status.company.com
- Social: @company on Twitter/X

---

**Report prepared by:** Incident Response Team  
**Reviewed by:** CTO, VP Engineering, VP Customer Support  
**Date:** January 20, 2026 - 8:00 PM EST
