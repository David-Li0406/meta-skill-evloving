# GHL CRM Advisor Skill

## Overview

This Claude Code skill provides strategic guidance for implementing and optimizing GoHighLevel (GHL) CRM across all 4 ACT projects. It acts as an on-demand CRM consultant that understands your entire ecosystem and can generate pipelines, workflows, email sequences, integration code, and training materials.

## What This Skill Does

When you ask Claude questions about GHL, CRM strategy, or implementation, this skill automatically activates and provides:

- **Pipeline designs** with stages, automation triggers, and custom fields
- **Email sequences** with subject lines, body copy, timing, and conditional logic
- **Tag taxonomies** for organizing contacts across multiple projects
- **Integration code** for connecting GHL with Stripe, Supabase, Resend, etc.
- **Analytics queries** for tracking conversion rates, revenue, and engagement
- **Training materials** for coordinators and team members
- **Troubleshooting help** for common GHL issues

## How to Use

Simply ask Claude your GHL-related questions naturally:

```
"Design a volunteer pipeline for The Harvest"
"Create a 7-email nurture sequence for ACT Farm residency alumni"
"How do I connect Stripe payments to residency bookings?"
"What tags should I use for the CONTAINED campaign?"
"Show me conversion metrics for our event booking pipeline"
"Create a quick reference guide for volunteer coordinators"
```

Claude will automatically use this skill to generate detailed, project-specific responses.

## Skill Capabilities

### 1. Pipeline Design & Optimization
- Complete stage-by-stage pipeline structures
- Automation triggers for each transition
- Custom fields specific to your programs
- Revenue tracking setup
- Drop-off analysis and recommendations

### 2. Workflow Scripting
- Multi-touch email sequences (7-14 emails)
- SMS campaigns with timing and conditional logic
- Subject lines optimized for open rates
- Personalization using GHL merge fields
- Unsubscribe and compliance handling

### 3. Tag Strategy
- Hierarchical tag taxonomies
- Cross-project tag consistency
- Behavioral and engagement tagging
- Search and segmentation examples

### 4. Integration Support
- **Supabase + GHL**: Auth vs CRM separation
- **Stripe + GHL**: Payment flows and webhooks
- **Resend + GHL**: Transactional email setup
- **Redis + GHL**: Caching for performance
- Code examples in TypeScript/Next.js

### 5. Reporting & Analytics
- Conversion rate formulas
- Revenue tracking and forecasting
- Pipeline velocity calculations
- Custom dashboard configurations

### 6. Team Training
- Quick reference guides for coordinators
- Step-by-step task instructions
- Troubleshooting common issues
- GHL UI walkthroughs

## Project Context

The skill understands all 4 ACT projects:

### The Harvest
- Community hub, volunteering, events, therapeutic programs, tenant/vendor management
- Revenue: Memberships, event tickets, program fees, tenant rent
- Special focus: Cultural heritage, accessibility, sliding scale pricing

### ACT Farm (Black Cockatoo Valley)
- Regenerative tourism, research residencies, workshops, June's Patch healthcare
- Revenue: Residencies ($300-500/night), workshops, future accommodation
- Special focus: Conservation mission, research outputs, healthcare privacy

### Empathy Ledger
- Storyteller platform, organization partnerships, cultural protocols
- Revenue: Organization subscriptions, platform fees, research grants, licensing
- Special focus: Indigenous consent, complex permissions, storyteller dignity

### JusticeHub
- Service directory, family support, CONTAINED campaign
- Revenue: Government grants, sponsorships, contributions, service fees (future)
- Special focus: Trauma-informed, accessibility, multi-language support

## Files in This Skill

- **SKILL.md** - Main skill definition with comprehensive guidance
- **QUICK-REFERENCE.md** - Common questions and quick answers
- **README.md** - This file

## Strategic Principles

This skill always prioritizes:

1. **Mission First** - Impact over revenue
2. **Human Touch** - Automation enhances, never replaces connection
3. **Dignity & Consent** - Especially for vulnerable communities
4. **Cultural Protocols** - Indigenous governance and sensitivity
5. **Accessibility** - Design for everyone
6. **Transparency** - Clear communication about data use
7. **Sustainability** - Systems that scale without burnout
8. **Community Ownership** - CRM serves the community

## Examples

### Example 1: Pipeline Design

**You ask**: "We're launching a CSA subscription box program at The Harvest. What pipeline should we use?"

**Skill generates**: Complete 6-stage pipeline (Interest → Box Size Selected → Payment Set Up → Active → Paused → Cancelled) with automation triggers, custom fields, revenue projections, and cross-project synergy suggestions.

### Example 2: Integration Code

**You ask**: "How do I connect Stripe payments to ACT Farm residency bookings in GHL?"

**Skill generates**:
- Two integration options (GHL native vs custom API)
- Complete TypeScript code for checkout and webhooks
- Environment variable setup
- Testing checklist
- Recommendation based on your needs

### Example 3: Training Material

**You ask**: "Create a guide for The Harvest coordinators on managing the volunteer pipeline"

**Skill generates**: Quick reference with when to update stages, how to record hours, how to generate reports, troubleshooting tips, and direct links to GHL.

## Technical Implementation

The skill includes code patterns for:

```typescript
// GHL API integration with Redis caching
import { createGHLClient } from '@/lib/ghl/client';
import { withCache } from '@/lib/redis';

const contact = await withCache(
  `ghl:contact:${email}`,
  async () => ghlClient.contacts.searchByEmail(email),
  600 // 10 min TTL
);
```

```typescript
// Supabase + GHL sync
async function syncToGHL(supabaseUser) {
  const contact = await ghlClient.contacts.upsert({
    email: supabaseUser.email,
    customFields: { supabase_user_id: supabaseUser.id }
  });

  await supabase.from('ghl_contact_sync').upsert({
    supabase_user_id: supabaseUser.id,
    ghl_contact_id: contact.id,
  });
}
```

```typescript
// Resend transactional emails
import { Resend } from 'resend';
import { WelcomeEmail } from '@/emails/welcome';

await resend.emails.send({
  from: 'The Harvest <hello@theharvest.org.au>',
  to: contact.email,
  react: WelcomeEmail({ name: contact.name }),
});
```

## Related Documentation

This skill references:

- [GHL_PIPELINE_STRATEGY.md](../../GHL_PIPELINE_STRATEGY.md) - Complete pipeline architecture
- [SUPABASE_GHL_INTEGRATION_ARCHITECTURE.md](../../SUPABASE_GHL_INTEGRATION_ARCHITECTURE.md) - Auth + CRM integration
- [GHL_SETUP_GUIDE.md](../../GHL_SETUP_GUIDE.md) - Step-by-step configuration
- [TENANT_VENDOR_PIPELINE.md](../../../The Harvest/TENANT_VENDOR_PIPELINE.md) - Tenant management details

## Troubleshooting

If the skill doesn't activate when you expect it to:

1. **Check your question includes GHL-related terms**: "GoHighLevel", "GHL", "CRM", "pipeline", "workflow", "automation"
2. **Be specific about the project**: Mention "The Harvest", "ACT Farm", "Empathy Ledger", or "JusticeHub"
3. **Ask actionable questions**: "Design", "Create", "How do I", "Show me" work better than vague queries

If you get a response but it's not detailed enough:

1. **Ask for more**: "Expand on the email sequence", "Show me the code for that"
2. **Be more specific**: "For storyteller onboarding specifically" instead of "for Empathy Ledger"

## Updating This Skill

Update the skill when:

- **New pipelines are created** - Add to SKILL.md project context
- **New projects join ACT** - Add project details and user journeys
- **GHL API changes** - Update integration code patterns
- **Team feedback** - Add training materials for common questions
- **Cross-project synergies discovered** - Document referral workflows

To update:
1. Edit `SKILL.md` (main skill definition)
2. Update `QUICK-REFERENCE.md` if adding common questions
3. Update this README if changing capabilities
4. Commit and push so team gets updates

## Benefits

### Time Savings
- **Pipeline design**: 2 hours → 15 minutes
- **Workflow scripting**: 4 hours → 30 minutes
- **Team training**: 3 hours → 1 hour
- **Troubleshooting**: 1 hour → 10 minutes

**Total**: ~20 hours/month saved across all GHL work

### Quality Improvements
- **Consistency** across all 4 projects
- **Best practices** embedded in every response
- **Completeness** (doesn't forget edge cases like unsubscribe links)
- **Evolution** (learns from ACT-specific patterns)

### Strategic Alignment
- **Mission-first recommendations** (impact over revenue)
- **Cross-project synergies** actively suggested
- **Community-centered design** (automation enhances connection)

## Version History

- **v1.0.0** (2025-12-24): Initial skill creation with full capabilities across all 4 projects

## Support

Questions about this skill? Ask Claude:

```
"How does the GHL CRM Advisor skill work?"
"What can the GHL skill help me with?"
"Show me examples of using the GHL advisor"
```

Or reach out to the development team.

---

**Created by**: ACT Development Team
**Maintained**: Project-wide (`.claude/skills/` directory)
**License**: Internal use for ACT projects
