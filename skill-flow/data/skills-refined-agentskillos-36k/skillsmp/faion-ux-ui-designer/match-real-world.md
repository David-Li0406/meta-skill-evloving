---
id: match-real-world
name: "Match Between System and Real World"
domain: UX
skill: faion-ux-ui-designer
category: "ux-design"
---

# Match Between System and Real World

## Metadata
- **Category:** UX / Usability Heuristic #2
- **Difficulty:** Beginner
- **Tags:** #methodology #ux #heuristics #nielsen-norman #language
- **Agent:** faion-usability-agent

---

## Problem

Users encounter unfamiliar jargon and technical terms. Icons and labels do not match what users expect. Information is organized in system-centric rather than user-centric ways. Concepts from the real world are misrepresented or ignored.

Without matching the real world:
- User confusion
- Learning curve increases
- Errors from misunderstanding
- Reduced adoption

---

## The Heuristic

**Usability Heuristic #2:** The design should speak the users' language, with words, phrases, and concepts familiar to the user, rather than internal jargon. Follow real-world conventions, making information appear in a natural and logical order.

---

## Framework

### Key Principles

1. **Use familiar language** - Words users actually use
2. **Follow conventions** - Match real-world expectations
3. **Logical information flow** - Natural order for users
4. **Meaningful metaphors** - Connect digital to physical

### Language Guidelines

| Instead of | Use |
|------------|-----|
| Terminate session | Log out |
| Execute query | Search |
| Invalid input | Please enter a valid email |
| Repository | Folder / Collection |
| Authenticate | Sign in |
| Synchronize | Update / Refresh |

### Conventions to Follow

| Domain | Convention |
|--------|------------|
| **E-commerce** | Shopping cart, checkout, wishlist |
| **Documents** | Files, folders, save, open |
| **Email** | Inbox, sent, draft, trash |
| **Social** | Friends, followers, like, share |
| **Navigation** | Home, back, menu, search |

---

## Implementation Patterns

### Natural Language

**Error messages:**
```
Bad: "Error 403: Authentication failed"
Good: "Incorrect password. Please try again."
```

**Labels:**
```
Bad: "DOB"
Good: "Date of birth"
```

**Instructions:**
```
Bad: "Input alphanumeric characters only"
Good: "Use only letters and numbers"
```

### Logical Information Order

**Address form:**
```
Bad: Country > State > City > Street > Zip
Good: Street > City > State > Zip > Country
(Matches how people think about addresses)
```

**Date selection:**
```
Cultural consideration:
US: Month / Day / Year
Europe: Day / Month / Year
Match user's locale
```

### Meaningful Icons

| Concept | Icon Should Represent |
|---------|----------------------|
| Save | Floppy disk (legacy) or cloud |
| Delete | Trash can |
| Settings | Gear |
| Search | Magnifying glass |
| Home | House |
| Close | X |

**Note:** Even if metaphor is outdated (floppy disk), users recognize it.

### Real-World Metaphors

**File management:**
- Desktop = workspace
- Folders = organization
- Trash = deletion (recoverable)

**E-commerce:**
- Cart = collecting items
- Checkout = payment area
- Wishlist = items for later

---

## Templates

### Language Audit Checklist

```markdown
# Language Audit: [Feature/Product]

**Date:** [Date]
**Reviewer:** [Name]

## Terminology Review

| Current Term | User-Friendly? | Suggested Alternative |
|--------------|----------------|----------------------|
| [Term] | Y/N | [Alternative] |

## Error Messages Review

| Current Message | Clear? | Suggested Improvement |
|-----------------|--------|----------------------|
| [Message] | Y/N | [Improvement] |

## Labels and Instructions

| Element | Issue | Recommendation |
|---------|-------|----------------|
| [Element] | [Issue] | [Fix] |

## Overall Recommendations
1. [Recommendation]
2. [Recommendation]
```

---

## Examples

### Good Examples

**Airbnb:**
- "Check in" / "Check out" (hotel terminology)
- "Guests" not "Users"
- "Listing" not "Property record"

**Gmail:**
- "Inbox" (physical mailbox)
- "Archive" (storing for later)
- "Snooze" (email reminder - sleep metaphor)

### Bad Examples

**Technical jargon:**
```
"Configure SMTP parameters for outbound mail relay"
→ Better: "Set up email sending"
```

**System-centric language:**
```
"Record created successfully"
→ Better: "Your booking is confirmed"
```

---

## Research Methods

### Finding User Language

1. **User interviews** - Listen to how they describe tasks
2. **Support tickets** - What terms do users use?
3. **Search logs** - What do they search for?
4. **Card sorting** - How do they categorize?
5. **Competitor analysis** - Industry standard terms

### Testing Language

1. **A/B testing** - Different label variations
2. **Comprehension testing** - Can users explain what it means?
3. **Task completion** - Does terminology help or hinder?

---

## Common Mistakes

1. **Internal jargon** - Using company-specific terms
2. **Technical language** - Developer/system terminology
3. **Abbreviations** - Unclear shortened forms
4. **Inconsistent terms** - Same thing called different names
5. **Culture blindness** - Not localizing properly

---

## Localization Considerations

- Translate meaning, not just words
- Adjust for cultural conventions
- Date and number formats
- Currency display
- Reading direction (LTR/RTL)
- Color meanings vary by culture

---

## Checklist

- [ ] All labels use user-friendly language
- [ ] Technical terms are avoided or explained
- [ ] Error messages are clear and helpful
- [ ] Information follows logical (user) order
- [ ] Icons match user expectations
- [ ] Metaphors are consistent and meaningful
- [ ] Language is consistent throughout
- [ ] Content is localized appropriately

---

## References

- UX research community: 10 Usability Heuristics
- Plain Language Guidelines
- Content Strategy for Mobile