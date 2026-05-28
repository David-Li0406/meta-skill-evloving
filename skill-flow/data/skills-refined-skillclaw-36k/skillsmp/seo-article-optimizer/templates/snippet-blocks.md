# Snippet Block Templates

Use these templates to structure content for featured snippet opportunities.

## Definition Block (40-60 words)

```markdown
**What is [Term]?**

[Term] is [concise definition that directly answers the query]. It [primary function/purpose] by [how it works]. [Key benefit or distinguishing characteristic]. This makes it [ideal use case or comparison point].
```

### Example

**What is Content Marketing?**

Content marketing is a strategic marketing approach focused on creating and distributing valuable, relevant content to attract and retain a target audience. It drives profitable customer action by building trust and authority. This makes it essential for long-term brand growth.

## Numbered Steps Block

```markdown
## How to [Action] in [Number] Steps

1. **[Step 1 Name]**: [One-sentence description of the action]
2. **[Step 2 Name]**: [One-sentence description of the action]
3. **[Step 3 Name]**: [One-sentence description of the action]
4. **[Step 4 Name]**: [One-sentence description of the action]
5. **[Step 5 Name]**: [One-sentence description of the action]
```

### Example

## How to Set Up Google Analytics in 5 Steps

1. **Create an account**: Sign up at analytics.google.com with your Google account
2. **Set up a property**: Add your website URL and configure basic settings
3. **Get tracking code**: Copy the measurement ID from your property settings
4. **Install the code**: Add the tracking snippet to your website's header
5. **Verify installation**: Use the Realtime report to confirm data is flowing

## Comparison Table Block

```markdown
## [Option A] vs [Option B]: Quick Comparison

| Feature | [Option A] | [Option B] |
|---------|------------|------------|
| [Feature 1] | [Value] | [Value] |
| [Feature 2] | [Value] | [Value] |
| [Feature 3] | [Value] | [Value] |
| Price | [Value] | [Value] |
| Best for | [Use case] | [Use case] |
```

### Example

## Notion vs Confluence: Quick Comparison

| Feature | Notion | Confluence |
|---------|--------|------------|
| Ease of use | Beginner-friendly | Steeper learning curve |
| Templates | 1000+ built-in | 75+ built-in |
| Integrations | 70+ native | 3000+ via Atlassian |
| Price | Free - $15/user/mo | $5.75 - $11/user/mo |
| Best for | Startups, small teams | Enterprise, Jira users |

## Bullet List Block

```markdown
## [Topic]: Key [Benefits/Features/Points]

- **[Point 1]**: [Brief explanation]
- **[Point 2]**: [Brief explanation]
- **[Point 3]**: [Brief explanation]
- **[Point 4]**: [Brief explanation]
- **[Point 5]**: [Brief explanation]
```

### Example

## Remote Work: Key Benefits for Employees

- **Flexibility**: Set your own schedule and work when you're most productive
- **No commute**: Save time and money by eliminating daily travel
- **Better work-life balance**: More time for family, hobbies, and self-care
- **Increased productivity**: Fewer office distractions and interruptions
- **Location independence**: Work from anywhere with an internet connection

## FAQ Block

```markdown
## Frequently Asked Questions

### [Question 1]?

[Direct, concise answer in 2-3 sentences]

### [Question 2]?

[Direct, concise answer in 2-3 sentences]

### [Question 3]?

[Direct, concise answer in 2-3 sentences]
```

### FAQ Schema (optional)

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[Question 1]?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Answer 1]"
      }
    }
  ]
}
```
