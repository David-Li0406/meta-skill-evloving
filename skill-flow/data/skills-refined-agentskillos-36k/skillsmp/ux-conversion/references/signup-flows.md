# Signup & Onboarding Flows

## Key Stats

- 80% abandon apps before using them due to bad onboarding
- 77% of users lost within first 3 days
- Time-to-value is the #1 predictor of retention

## Signup Flow Principles

| Principle | Implementation |
|-----------|---------------|
| **Minimize fields** | Name, email, password only at signup |
| **Social login** | 8% signup rate boost; reduces friction |
| **Progress indicators** | "Step 2 of 3" reduces anxiety |
| **No credit card upfront** | Remove barriers to trial |
| **Single-column layout** | Clear visual path |
| **Guest checkout** | Make prominent for e-commerce |

## Signup Field Priority

```
Essential (signup):
- Email
- Password

Collect during onboarding:
- Name
- Company (if B2B)
- Role/use case
- Preferences

Collect later / progressively:
- Phone
- Address
- Payment info
```

## Onboarding Flow Principles

| Principle | Implementation |
|-----------|---------------|
| **Time-to-value** | First win in < 60 seconds |
| **Progressive disclosure** | Don't explain everything upfront |
| **Personalization** | 2-5 options for user type; tailor flow |
| **Interactive tours** | 3-5 tooltips max; action-oriented |
| **Checklists** | Visual progress toward setup completion |
| **Skip option** | Let experienced users bypass |
| **Celebrate success** | Acknowledge milestones |

## Onboarding Patterns

### Welcome Survey (Personalization)
```
"What brings you here today?"
- [ ] Personal project
- [ ] Work/business
- [ ] Just exploring

→ Tailors subsequent onboarding
```

### Setup Checklist
```
Get started (2 of 4 complete)
✓ Create account
✓ Verify email
○ Connect your first integration
○ Invite team members
```

### Product Tour
- 3-5 steps maximum
- Each step requires action, not just reading
- Always show "Skip tour" option
- Highlight one feature at a time

### Empty States
Turn blank screens into onboarding:
```
"No projects yet"
↓
"Create your first project to get started"
[Create project] button
```

## Multi-Step Form Pattern

```
Step 1: Account (email, password)
        ↓
Step 2: Profile (name, role)  [can skip]
        ↓
Step 3: Preferences (notifications, theme)  [can skip]
        ↓
Step 4: First action (create first item)
        ↓
Dashboard with checklist
```

## Reducing Signup Friction

| Friction Point | Solution |
|----------------|----------|
| Too many fields | Defer to onboarding |
| Password requirements | Show requirements upfront, validate inline |
| Email verification | Allow limited access before verified |
| Captcha | Use invisible reCAPTCHA |
| Terms checkbox | Link text, not required checkbox |

## Success Metrics

| Metric | Target |
|--------|--------|
| Signup completion | > 80% |
| Onboarding completion | > 60% |
| Time to first value | < 60 seconds |
| Day 1 retention | > 40% |
| Day 7 retention | > 20% |

## Anti-Patterns

- Forcing full profile before showing value
- Tour with 10+ steps
- No way to skip onboarding
- Requiring credit card for free trial
- Email verification blocking all access
- Overwhelming with features on first visit
