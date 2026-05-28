---
name: code-quality
description: Maintain high standards in the OutreachGlobal Nx monorepo with best practices and consistency
---

# Code Quality Enforcement Instructions

## Purpose
Ensure consistent, maintainable, and high-quality code across the OutreachGlobal Nx monorepo, following TypeScript, React, and Node.js best practices while maintaining multi-tenant security.

## When to Use This Skill
- Code reviews and pull requests
- New feature development
- Refactoring existing code
- Setting up new projects/apps
- Establishing team coding standards

## Code Quality Standards

### 1. TypeScript Best Practices
**Strict mode compliance:**
```typescript
// ✅ Required: Strict type checking
interface User {
  readonly id: string;
  readonly email: string;
  readonly teamId: string;
  readonly createdAt: Date;
}

// ❌ Avoid: Any types
const user: any = getUser(); // Use proper typing

// ✅ Use: Union types for clarity
type CampaignStatus = 'draft' | 'active' | 'paused' | 'completed';
```

### 2. React Component Patterns
**Modern React patterns:**
```typescript
// ✅ Functional components with hooks
const CampaignForm: React.FC<CampaignFormProps> = ({ onSubmit }) => {
  const [formData, setFormData] = useState<CampaignData>({
    name: '',
    teamId: ''
  });

  const handleSubmit = useCallback(async (e: FormEvent) => {
    e.preventDefault();
    await onSubmit(formData);
  }, [formData, onSubmit]);

  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
    </form>
  );
};
```

### 3. Error Handling Standards
**Consistent error handling:**
```typescript
// ✅ Structured error handling
try {
  const result = await processCampaign(campaignId);
  return { success: true, data: result };
} catch (error) {
  console.error(`Campaign processing failed: ${campaignId}`, error);

  if (error instanceof ValidationError) {
    return { success: false, error: 'Invalid campaign data' };
  }

  if (error instanceof DatabaseError) {
    return { success: false, error: 'Database connection failed' };
  }

  return { success: false, error: 'Internal server error' };
}
```

### 4. Database Query Patterns
**Drizzle ORM best practices:**
```typescript
// ✅ Proper query building
const getLeadsByTeam = async (teamId: string, limit = 50) => {
  return await db
    .select({
      id: leadsTable.id,
      name: leadsTable.name,
      status: leadsTable.status,
      createdAt: leadsTable.createdAt
    })
    .from(leadsTable)
    .where(eq(leadsTable.teamId, teamId))
    .orderBy(desc(leadsTable.createdAt))
    .limit(limit);
};

// ✅ Use transactions for related operations
await db.transaction(async (tx) => {
  const campaign = await tx.insert(campaignsTable).values(campaignData).returning();
  await tx.insert(campaignLeadsTable).values(
    leadIds.map(leadId => ({
      campaignId: campaign[0].id,
      leadId
    }))
  );
});
```

## Nx Monorepo Standards

### Project Structure
**Consistent app/lib organization:**
```
apps/
├── api/                    # NestJS backend
│   ├── src/
│   │   ├── app/           # Feature modules
│   │   ├── lib/           # Shared utilities
│   │   └── main.ts
│   └── project.json
├── front/                  # Next.js frontend
│   ├── src/
│   │   ├── app/           # App router pages
│   │   ├── components/    # Reusable components
│   │   └── lib/           # Utilities
│   └── project.json
```

### Dependency Management
**pnpm workspace rules:**
- Use workspace dependencies for internal packages
- Keep dependencies up to date
- Audit for security vulnerabilities regularly
- Minimize bundle size with tree shaking

## Testing Standards

### Unit Test Coverage
**Minimum 80% coverage:**
```typescript
// ✅ Comprehensive testing
describe('CampaignService', () => {
  let service: CampaignService;
  let mockDb: MockProxy<DrizzleDB>;

  beforeEach(() => {
    mockDb = mock<DrizzleDB>();
    service = new CampaignService(mockDb);
  });

  it('should create campaign with valid data', async () => {
    const campaignData = { name: 'Test Campaign', teamId: 'team-1' };
    mockDb.insert.mockResolvedValue([campaignData]);

    const result = await service.createCampaign(campaignData);

    expect(result).toEqual(campaignData);
    expect(mockDb.insert).toHaveBeenCalledWith(campaignsTable, campaignData);
  });
});
```

### Integration Testing
**API endpoint testing:**
```typescript
describe('POST /api/campaigns', () => {
  it('should create campaign for authenticated user', async () => {
    const response = await request(app)
      .post('/api/campaigns')
      .set('Authorization', `Bearer ${token}`)
      .send({ name: 'Test Campaign' });

    expect(response.status).toBe(201);
    expect(response.body).toHaveProperty('id');
  });
});
```

## Code Review Checklist

### General
- [ ] TypeScript strict mode enabled
- [ ] No any types without justification
- [ ] Proper error handling with try/catch
- [ ] Consistent naming conventions (camelCase, PascalCase)
- [ ] No console.log in production code

### React Specific
- [ ] Functional components preferred
- [ ] Proper dependency arrays in useEffect/useCallback
- [ ] No unnecessary re-renders
- [ ] Accessible components (ARIA labels, keyboard navigation)

### Backend Specific
- [ ] Input validation with Zod schemas
- [ ] Proper HTTP status codes
- [ ] Database transactions for related operations
- [ ] No SQL injection vulnerabilities

### Security
- [ ] No hardcoded secrets
- [ ] Proper authentication checks
- [ ] Input sanitization
- [ ] CORS properly configured

## Performance Standards

### Frontend
- Bundle size < 500KB
- First contentful paint < 2 seconds
- Lighthouse score > 90

### Backend
- API response time < 500ms
- Memory usage monitored
- Database query optimization
- Proper indexing

## Response Format
When reviewing code quality, provide:
1. **Quality score** (A/B/C grade with breakdown)
2. **Critical issues** requiring immediate fixes
3. **Improvement suggestions** with code examples
4. **Best practice compliance** percentage
5. **Testing recommendations** for coverage gaps

## Related Skills
- Use with `security-scan` for vulnerability assessment
- Combine with `schema-audit` for database code quality
- Reference `multi-tenant-audit` for tenant isolation in code