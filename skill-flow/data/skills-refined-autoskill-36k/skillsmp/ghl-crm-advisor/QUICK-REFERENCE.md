# GHL CRM Quick Reference

## Common Skill Invocations

### Pipeline Design
```
"Design a pipeline for [program/initiative] at [project]"
"What stages should we use for [user journey]?"
"How should we track [specific program] in GHL?"
```

### Workflow Creation
```
"Create an email sequence for [user type]"
"Write a nurture campaign for [program] alumni"
"What automations should trigger when [event happens]?"
```

### Integration Questions
```
"How do I connect [tool] to GHL?"
"Set up Stripe payments for [booking/subscription]"
"Sync Supabase users with GHL contacts"
```

### Tag Strategy
```
"What tags should I use for [program/campaign]?"
"How do I organize tags across multiple projects?"
"Create a tag taxonomy for [use case]"
```

### Reporting
```
"Show me conversion metrics for [pipeline]"
"How do I track revenue from [program]?"
"Create a report for [stakeholder/grant application]"
```

### Training
```
"Create a guide for [role] on how to [task]"
"Troubleshoot: [specific issue]"
"Explain [GHL feature] to non-technical team"
```

## Quick Answers

### When should I use GHL vs Supabase?

**Use GHL for**:
- Marketing automation (email sequences, SMS campaigns)
- Lead nurturing and sales pipelines
- Event/service booking and scheduling
- General contact management
- Revenue tracking and reporting

**Use Supabase for**:
- Platform authentication (login/signup)
- Complex permissions (RLS, cultural protocols)
- User-generated content storage
- Real-time features
- Database-driven applications

**Use both when**:
- Platform has user accounts (Supabase) AND you want to market to those users (GHL)
- Example: Empathy Ledger storytellers log in via Supabase, organization leads are nurtured via GHL

### What's the recommended email setup?

**Use Resend for**:
- ALL transactional emails (welcome, password reset, confirmations, receipts)
- System notifications (application approved, payment processed)
- User-initiated emails (inquiry form submissions)

**Use GHL for**:
- Marketing campaigns (newsletters, promotional offers)
- Nurture sequences (multi-touch lead warming)
- Triggered workflows (tag-based automation)

**Why separate?**:
- Higher deliverability (transactional from Resend, marketing from GHL)
- Better open rates (users expect transactional emails)
- Clearer analytics (separate metrics for each type)

### How do I handle cross-project referrals?

1. **Tag contacts with interests**: `interest:conservation`, `interest:storytelling`, `interest:social-justice`
2. **Create cross-project workflows**:
   - The Harvest volunteer tagged `interest:conservation` → Trigger workflow: "Invite to ACT Farm workshop"
   - ACT Farm resident tagged `interest:storytelling` → Trigger workflow: "Introduce to Empathy Ledger"
3. **Use multi-project tags**: `cross-project:active` for contacts engaged with 2+ projects
4. **Revenue tracking**: Attribute referrals with custom field `referred_from` = "the-harvest"

### What's the typical pipeline structure?

**Standard 7-stage funnel** (adapt as needed):

1. **Inquiry** - First contact, expressed interest
2. **Qualified** - Meets criteria, worth pursuing
3. **Engaged** - Responded positively, active conversation
4. **Application/Booking** - Filled out form, committed to next step
5. **Approved/Confirmed** - Accepted, date set, payment pending
6. **Active/Completed** - Participating, service delivered
7. **Alumni** - Program finished, stay connected

**Variations**:
- Add "Waitlist" between Qualified and Engaged (for limited capacity)
- Add "Payment Received" between Approved and Active (for prepay programs)
- Add "Paused" parallel to Active (for subscriptions, memberships)
- Split Alumni into "Inactive" and "Return Customer"

### How often should I clean my pipelines?

**Weekly**: Review "stuck" contacts (same stage >30 days)
- Move forward, move to inactive, or mark as "dead lead"

**Monthly**: Archive completed/lost opportunities
- Clear pipeline for current focus
- Run reports on closed deals

**Quarterly**: Tag taxonomy review
- Consolidate redundant tags
- Add new tags for emerging patterns
- Update workflow triggers based on tag changes

## GHL API Rate Limits

- **100 requests per minute** per location
- **10,000 requests per day** per location

**Best practices**:
- Use Redis caching (10-minute TTL for contact lookups)
- Batch updates when possible
- Use webhooks instead of polling
- Implement exponential backoff on failures

## Common Custom Fields by Project

### The Harvest
- `volunteer_skills` (text: gardening, cooking, admin, teaching)
- `availability` (dropdown: weekday/weekend/flexible)
- `t_shirt_size` (dropdown: XS-3XL)
- `total_volunteer_hours` (number)
- `membership_level` (dropdown: Friend/Supporter/Patron)
- `dietary_requirements` (text)

### ACT Farm
- `residency_type` (dropdown: R&D/Creative/Wellbeing/Research)
- `research_focus` (text)
- `arrival_date` (date)
- `nights_booked` (number)
- `accommodation_needs` (text: accessibility, dietary)
- `payment_status` (dropdown: pending/deposit/fully_paid)

### Empathy Ledger
- `organization_type` (dropdown: NGO/Education/Media/Research/Government)
- `storyteller_count_interest` (number: how many storytellers they want access to)
- `use_case` (text: campaign, research, education, etc.)
- `contract_value` (number: $)
- `supabase_user_id` (text: for sync)

### JusticeHub
- `family_need` (dropdown: housing/legal/mental-health/employment)
- `service_provider_category` (dropdown: legal/housing/healthcare/etc.)
- `campaign_role` (dropdown: nominee/nominator/attendee/advocate)
- `politician_level` (dropdown: local/state/federal)
- `media_type` (dropdown: print/broadcast/online/social)

## Workflow Naming Convention

```
[Project]-[Type]-[Trigger]

Examples:
- harvest-welcome-volunteer-signup
- actfarm-nurture-residency-alumni
- empathy-reminder-profile-completion
- justicehub-campaign-nomination-received
```

**Why this matters**: Easy filtering, clear purpose, team collaboration

## Testing Checklist

Before launching a new pipeline/workflow:

- [ ] Test form submission creates contact
- [ ] Verify tags are applied correctly
- [ ] Check contact lands in correct pipeline stage
- [ ] Confirm first automation email sends within expected time
- [ ] Test conditional logic (if X, then Y)
- [ ] Verify unsubscribe link works
- [ ] Check mobile email rendering
- [ ] Test with various email providers (Gmail, Outlook, Apple Mail)
- [ ] Confirm webhook signatures are validated
- [ ] Load test (submit 10+ contacts rapidly)

## Emergency Contacts

**GHL Support**: https://support.gohighlevel.com/
**API Status**: https://status.gohighlevel.com/
**Community Forum**: https://www.facebook.com/groups/gohighlevel

**Internal**:
- GHL Admin: [Your team member]
- Developer (API issues): [Your developer]
- Coordinator (pipeline questions): [Your coordinator]

## Useful GHL UI Shortcuts

- **Search contacts**: `Cmd/Ctrl + K` → type name/email
- **Create contact**: Click "Contacts" → `+` button (top right)
- **View pipeline**: Click "Opportunities" → Select pipeline from dropdown
- **Run workflow manually**: Contact → Workflows tab → "Enroll" button
- **Check automation history**: Contact → Timeline tab
- **Export contacts**: Contacts → Filters → "Export CSV" button
- **Duplicate workflow**: Workflows → `...` menu → "Clone"

## Pro Tips

1. **Start simple**: Don't over-automate on day 1. Add complexity as you learn patterns.

2. **Human override**: Always allow coordinators to manually progress contacts, even with automation.

3. **Personal touch**: Automate the routine, personalize the important. Example: Automated reminder emails, personal phone call for high-value leads.

4. **Test everything**: Use test contacts (your own email with +tag, e.g., `you+test@email.com`) before going live.

5. **Monitor daily**: Check automation logs daily for first 2 weeks, then weekly.

6. **Ask for feedback**: Monthly check-in with team: "What's working? What's frustrating?"

7. **Celebrate wins**: Share success stories ("GHL helped us book 10 residencies this month!") to build team buy-in.

## Version History

- v1.0.0 (2025-12-24): Initial quick reference guide
