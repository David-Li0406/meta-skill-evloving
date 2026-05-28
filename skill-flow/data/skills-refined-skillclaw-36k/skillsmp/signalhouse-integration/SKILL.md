---
name: signalhouse-integration
description: Maintain 1:1 mapping between Nextier teams and SignalHouse SubGroups for proper multi-tenant isolation
---

# SignalHouse Integration Management

## Core Principle
**Nextier Team = SignalHouse SubGroup (1:1 Mapping)**

Every Nextier team must have exactly one corresponding SignalHouse SubGroup for complete isolation of SMS campaigns, phone numbers, and analytics.

## When to Use This Skill
- Creating new Nextier teams
- Managing SignalHouse API integrations
- Debugging campaign delivery issues
- Setting up new phone numbers or brands
- Troubleshooting webhook events

## Team Creation Workflow

### 1. Nextier Team Setup
```typescript
// When a new team is created in Nextier
const team = await createTeam({
  name: "ABC Realty",
  // ... other team data
});

// Immediately create corresponding SignalHouse SubGroup
const subGroup = await signalhouse.createSubGroup({
  name: team.name,
  // Map 1:1 with Nextier team
});

// Store the mapping
await db.update(teamsTable).set({
  signalhouseSubGroupId: subGroup.id
}).where(eq(teamsTable.id, team.id));
```

### 2. SubGroup Configuration
**Required Setup per SubGroup:**
- **Brands**: 10DLC registration for SMS compliance
- **Phone Numbers**: Dedicated pool for the team
- **Campaigns**: Use case compliance settings
- **Webhooks**: Delivery and response event handling

## Integration Points

### API Endpoints to Monitor
- `/api/signalhouse/campaigns/*` - Campaign creation and management
- `/api/signalhouse/webhooks/*` - Inbound event processing
- `/api/teams/*` - Team lifecycle management

### Database Schema Requirements
```sql
-- teams table must include SignalHouse mapping
ALTER TABLE teams ADD COLUMN signalhouse_sub_group_id VARCHAR(255);

-- All SignalHouse operations must filter by this ID
SELECT * FROM campaigns WHERE signalhouse_sub_group_id = ?
```

## Common Issues & Solutions

### Issue: SubGroup Not Created
**Symptoms:** Campaigns fail with "SubGroup not found"
**Solution:** Ensure `signalhouse.createSubGroup()` is called immediately after `createTeam()`

### Issue: Webhook Mismatch
**Symptoms:** Events not reaching correct team
**Solution:** Verify webhook URLs include team identification

### Issue: Phone Number Conflicts
**Symptoms:** Numbers shared across teams
**Solution:** Each SubGroup must have dedicated number pool

### Issue: Campaign Compliance
**Symptoms:** SMS blocked by carriers
**Solution:** Proper 10DLC registration per SubGroup

## Audit Checklist

- [ ] Every Nextier team has `signalhouseSubGroupId`
- [ ] No orphaned SubGroups without Nextier teams
- [ ] Webhook endpoints properly namespaced
- [ ] Phone numbers not shared between SubGroups
- [ ] Campaign creation includes SubGroup context

## API Integration Best Practices

### Error Handling
```typescript
try {
  const result = await signalhouse.createCampaign(campaignData);
  // Store campaign with subGroupId
  await db.insert(campaignsTable).values({
    ...campaignData,
    signalhouseSubGroupId: team.signalhouseSubGroupId,
    signalhouseCampaignId: result.id
  });
} catch (error) {
  // Log with team context for debugging
  console.error(`SignalHouse error for team ${team.id}:`, error);
}
```

### Rate Limiting
- Respect SignalHouse API limits
- Implement exponential backoff for retries
- Monitor API usage per SubGroup

### Monitoring
- Track delivery rates per SubGroup
- Monitor webhook health
- Alert on SubGroup mapping issues

## Testing Requirements

### Unit Tests
- Mock SignalHouse API responses
- Test SubGroup creation on team setup
- Verify proper error handling

### Integration Tests
- End-to-end campaign creation
- Webhook event processing
- Multi-tenant isolation verification

## Related Skills
- Use with `multi-tenant-audit` for data isolation
- Combine with `campaign-optimizer` for performance
- Reference `cost-guardian` for API usage monitoring