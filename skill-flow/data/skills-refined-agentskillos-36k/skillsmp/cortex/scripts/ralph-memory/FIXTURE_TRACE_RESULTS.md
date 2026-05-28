# Cortex Memory System - Fixture Trace Results

Generated: 2026-01-22

This document shows the full transformation pipeline for each test fixture using **real data from Tyler's communications**.

---

## 1. imessage/identity-disclosure

### Raw Input
```
Thread: imessage:+18313452220
Reference Time: 2025-04-18T15:00:00Z

[Tyler → Joe Schooler] 14:56:22
"Tnapathy@gmail.com is my personal email"

[Joe Schooler → Tyler] 14:58:18
"Thanks man! Ill send you an email with some prds on the concepts, no need for a NDA!"
```

### Extracted Graph

**Entities:**
| Name | Type | ID |
|------|------|-----|
| Tyler | Person | `8d1bbeb9-...` |
| Joe Schooler | Person | `c178e1b0-...` |
| prds | Document | `0eb37eec-...` |

**Relationships:**
```
Joe Schooler -[REFERENCES]-> prds
```

**Aliases Created:**
| Entity | Alias | Type |
|--------|-------|------|
| Tyler | Tnapathy@gmail.com | email |
| Tyler | Tyler | name |
| Joe Schooler | Joe Schooler | name |

**Relationship Mentions (Provenance):**
| Fact | Source Type | Relationship ID |
|------|-------------|-----------------|
| Tyler's email is Tnapathy@gmail.com | `self_disclosed` | `null` (identity → alias) |
| Joe Schooler will send prds to Tyler | `mentioned` | `872a14c9-...` |

### Key Observations
- ✅ Email correctly promoted to `entity_aliases` (not stored in relationships)
- ✅ Source type correctly identified as `self_disclosed` (Tyler said it about himself)
- ✅ `relationship_id = null` for identity extractions (they go to aliases, not relationships table)

---

## 2. imessage/job-change

### Raw Input
```
Thread: imessage:+14123035909
Reference Time: 2025-09-06T00:00:00Z

[Tyler → Iris] 21:37:07
"Talked to Chris again and the first number he threw out was like 280k TC which is like fully 70k less than when I left Apple"

[Iris → Tyler] 21:38:31
"I wil talk to him later today"

[Iris → Tyler] 21:39:25
"Thats also less than your current comp so tell him that also"

[Tyler → Iris] 21:41:02
"I did"
```

### Extracted Graph

**Entities:**
| Name | Type | ID |
|------|------|-----|
| Tyler | Person | `b273864f-...` |
| Iris | Person | `7f9a8cc0-...` |
| Chris | Person | `43ff2530-...` |
| Apple | Company | `c09b850e-...` |

**Relationships:**
```
Tyler -[KNOWS]-> Chris
Tyler -[WORKS_AT]-> Apple (past tense detected)
Iris -[KNOWS]-> Chris
```

**Aliases Created:**
| Entity | Alias | Type |
|--------|-------|------|
| Tyler | Tyler | name |
| Iris | Iris | name |
| Chris | Chris | name |
| Apple | Apple | name |

**Relationship Mentions (Provenance):**
| Fact | Source Type | Relationship ID |
|------|-------------|-----------------|
| Tyler talked to Chris | `self_disclosed` | `ad0b8e30-...` |
| Tyler used to work at Apple | `mentioned` | `26949f7f-...` |
| Iris will talk to Chris | `self_disclosed` | `52e2861a-...` |

### Key Observations
- ✅ Past tense "left Apple" correctly extracted as WORKS_AT relationship
- ✅ Company entity (Apple) properly typed
- ✅ Third-party (Chris) extracted from context
- ⚠️ Compensation details (280k TC, 70k less) not extracted as literals (could be enhanced)

---

## 3. imessage/social-relationship

### Raw Input
```
Thread: imessage:chat300385060851851889 (Group Chat)
Reference Time: 2026-01-01T00:00:00Z

[Unknown → Group] 00:39:28
"https://venmo.com/u/Casexadams"

[Tyler → Group] 00:55:58
"TLC option, walking up"

[Unknown → Group] 12:45:52
"Everyone pay casey if you didn't yet!"

[Unknown → Group] 18:17:51
"Marty Supreme on Sunday at 6:15. Any takers?"

[Tyler → Group] 18:20:40
"I'll be there"
```

### Extracted Graph

**Entities:**
| Name | Type | ID |
|------|------|-----|
| Tyler | Person | `b17dd2ef-...` |
| Casey | Person | `9a34d218-...` |
| Casexadams | Person | `a7332187-...` |
| Marty Supreme | Event | `dec564ca-...` |

**Relationships:**
```
Tyler -[ATTENDED]-> Marty Supreme
```

**Aliases Created:**
| Entity | Alias | Type |
|--------|-------|------|
| Tyler | Tyler | name |
| Casey | Casey | name |
| Casexadams | Casexadams | name |
| Casexadams | @Casexadams | handle |
| Marty Supreme | Marty Supreme | name |

**Relationship Mentions (Provenance):**
| Fact | Source Type | Relationship ID |
|------|-------------|-----------------|
| Casexadams has Venmo handle @Casexadams | `self_disclosed` | `null` (→ alias) |
| Tyler will attend Marty Supreme | `self_disclosed` | `b2181bbd-...` |

### Key Observations
- ✅ Venmo handle extracted from URL and promoted to alias
- ✅ Event entity (Marty Supreme) correctly typed
- ⚠️ Casey and Casexadams not merged (need merge_candidate system)
- ✅ Future attendance correctly extracted with temporal context

---

## 4. gmail/work-thread

### Raw Input
```
Thread: gmail:199ee12a686318d1
Reference Time: 2025-10-16T17:34:42Z

From: Tyler Brandt <tnapathy@gmail.com>
To: charley.griffiths@clearme.com
Subject: Meeting with Jeff/Vlad

"Hey Charley,

Thanks for clarifying the policy issue.
My last day is next Tuesday (Oct 22nd), so I'm free to meet any time
Wednesday onwards.

I have a time-sensitive proposal that could benefit CLEAR in both the short
and long term, so ideally we'd connect that day/week.
I am flexible and can make any time Wed-Fri work. Happy to work around
their schedules.

Thanks for coordinating this,
Tyler"
```

### Extracted Graph

**Entities:**
| Name | Type | ID |
|------|------|-----|
| Tyler Brandt | Person | `c3083c51-...` |
| Charley | Person | `366e6648-...` |
| CLEAR | Company | `825c0e8a-...` |

**Relationships:**
```
Tyler Brandt -[CUSTOMER_OF]-> CLEAR
Tyler Brandt -[KNOWS]-> Charley
Tyler Brandt -[ENDED_ON]-> "2025-10-22" (job end date literal)
```

**Aliases Created:**
| Entity | Alias | Type |
|--------|-------|------|
| Tyler Brandt | Tyler Brandt | name |
| Charley | Charley | name |
| CLEAR | CLEAR | name |

**Relationship Mentions (Provenance):**
| Fact | Source Type | Relationship ID |
|------|-------------|-----------------|
| Tyler Brandt mentions CLEAR as a company that could benefit | `mentioned` | `a092e58f-...` |
| Tyler Brandt knows Charley | `mentioned` | `e0ca5b3f-...` |
| Tyler Brandt's last day of work is October 22nd | `self_disclosed` | `3d2ca672-...` |

### Key Observations
- ✅ Company (CLEAR) correctly extracted from email context
- ✅ Job end date captured as literal relationship
- ✅ Email recipient (Charley) extracted as entity
- ⚠️ Jeff/Vlad from subject not extracted (could be enhanced)

---

## 5. gmail/newsletter-sender (Cloudflare Invoice)

### Raw Input
```
Thread: gmail:19bbe137219bab27
Reference Time: 2026-01-14T19:55:02Z

From: Cloudflare <noreply@notify.cloudflare.com>
To: tnapathy@gmail.com
Subject: Your Cloudflare invoice is available

"Your Cloudflare invoice for January 2026 is now available.

Account: Tyler Brandt (tnapathy@gmail.com)
Invoice Period: January 2026
Service: Cloudflare Pro Plan

View your invoice in the Cloudflare dashboard.

Cloudflare, Inc.
101 Townsend St
San Francisco, CA 94107"
```

### Extracted Graph

**Entities:**
| Name | Type | ID |
|------|------|-----|
| Tyler Brandt | Person | `52220e53-...` |
| Cloudflare | Company | `ba461172-...` |
| Cloudflare, Inc. | Company | `2fb2d95c-...` |
| Cloudflare Pro Plan | Project | `0a8f477c-...` |
| Cloudflare dashboard | Project | `82cc0901-...` |
| 101 Townsend St | Location | `958359c9-...` |
| San Francisco, CA 94107 | Location | `be561217-...` |

**Relationships:**
```
Tyler Brandt -[CUSTOMER_OF]-> Cloudflare
Tyler Brandt -[USES]-> Cloudflare Pro Plan (valid_at: 2026-01)
Cloudflare -[OWNS]-> Cloudflare Pro Plan
Cloudflare -[OWNS]-> Cloudflare dashboard
Cloudflare, Inc. -[LOCATED_IN]-> 101 Townsend St
101 Townsend St -[LOCATED_IN]-> San Francisco, CA 94107
```

**Aliases Created:**
| Entity | Alias | Type |
|--------|-------|------|
| Tyler Brandt | Tyler Brandt | name |
| Cloudflare | Cloudflare | name |
| Cloudflare, Inc. | Cloudflare, Inc. | name |
| etc. | ... | ... |

**Relationship Mentions (Provenance):**
| Fact | Source Type | Relationship ID |
|------|-------------|-----------------|
| Tyler Brandt has email tnapathy@gmail.com | `mentioned` | `null` |
| Tyler Brandt is a customer of Cloudflare | `inferred` | `89841aef-...` |
| Tyler Brandt uses Cloudflare Pro Plan | `inferred` | `aa5ba4b8-...` |
| Cloudflare, Inc. is located at 101 Townsend St | `mentioned` | `93e1626c-...` |

### Key Observations
- ✅ Company and product entities correctly extracted
- ✅ Location hierarchy preserved (street → city)
- ⚠️ Cloudflare vs Cloudflare, Inc. not merged (merge_candidate needed)
- ✅ Temporal context (January 2026) captured in relationship

---

## 6. aix/personal-info (Wire Fraud Document)

### Raw Input
```
Thread: imessage:+16319056994
Reference Time: 2025-12-26T00:00:00Z

[Casey → Tyler]
"In October 2025, Thomas S. Prendergast (DOB: 05/22/1972, of 117 S. Fairview Ave, 
Bayport, NY 11705, phone: 516-617-2280, email: prendergastdev@gmail.com) induced 
William T. Adams to wire $100,000..."

[Full legal document with extensive PII, bank accounts, court cases...]
```

### Extracted Graph

**Entities:**
| Name | Type | ID |
|------|------|-----|
| Thomas S. Prendergast | Person | `99055356-...` |
| William T. Adams | Person | `e9d6ba42-...` |
| Lauren Taylor | Person | `2f7ad2ca-...` |
| Stuart Morgen | Person | `19c9960d-...` |
| Capital One | Company | `47d467f5-...` |
| JPMorgan Chase | Company | `236dbb0d-...` |
| Nassau County Supreme Court | Company | `6b3cd6a4-...` |
| Bayport, NY | Location | `cc617eaa-...` |
| Riverhead, NY | Location | `1b9d88a6-...` |
| 117 S. Fairview Ave | Location | `1c9dea4b-...` |
| Eastern District of NY | Location | `a313d325-...` |

**Relationships:**
```
Thomas S. Prendergast -[KNOWS]-> William T. Adams (valid_at: 2025-10)
Thomas S. Prendergast -[LIVES_IN]-> Bayport, NY
Thomas S. Prendergast -[LIVES_IN]-> 117 S. Fairview Ave
Thomas S. Prendergast -[BORN_ON]-> "1972-05-22"
Thomas S. Prendergast -[LOCATED_IN]-> Eastern District of NY (valid_at: 2025-12)
William T. Adams -[CUSTOMER_OF]-> Capital One (valid_at: 2025-10-21)
William T. Adams -[CUSTOMER_OF]-> JPMorgan Chase (valid_at: 2025-10-21)
William T. Adams -[LIVES_IN]-> Riverhead, NY
Stuart Morgen -[KNOWS]-> Thomas S. Prendergast
```

**Relationship Mentions (Provenance):**
| Fact | Source Type | Relationship ID |
|------|-------------|-----------------|
| Thomas S. Prendergast has the email prendergastdev@gmail.com | `mentioned` | `null` |
| Thomas S. Prendergast has the phone number 516-617-2280 | `mentioned` | `null` |
| Thomas S. Prendergast was born on 1972-05-22 | `mentioned` | `7b80f759-...` |
| William T. Adams wired money from Capital One | `mentioned` | `d59b960b-...` |
| Stuart Morgen is suing Thomas S. Prendergast | `mentioned` | `c34d8bb1-...` |

### Key Observations
- ✅ **11 entities** extracted from complex legal document
- ✅ DOB correctly extracted as BORN_ON relationship with date literal
- ✅ Multiple location types (city, address) correctly typed
- ✅ Bank relationships captured with temporal context
- ✅ Phone and email captured in relationship mentions (promoted to aliases)
- ⚠️ Account numbers not extracted as sensitive literals (may need explicit support)

---

## 7. aix/project-discussion

### Raw Input
```
Thread: cursor:session-memory-planning
Reference Time: 2025-12-15T00:00:00Z

[Tyler discussing memory system architecture]
"I have an app that has total context about all my imessages, instantly as they come in. 
And it has total historic knowledge of my chat history across all of my contacts.

I want to develop a feature on top of this context that for every single incoming message, 
I take some set of context... and then based on the current conversation offer some 
suggested prompts/actions for the user to go deeper.

So like, if me and my girlfriend are wondering where we should go to dinner..."
```

### Extracted Graph

**Entities:**
| Name | Type | ID |
|------|------|-----|
| Tyler | Person | `69d66e5d-...` |
| Girlfriend | Person | `111b4797-...` |

**Relationships:**
```
Tyler -[DATING]-> Girlfriend
```

**Aliases Created:**
| Entity | Alias | Type |
|--------|-------|------|
| Tyler | Tyler | name |
| Girlfriend | Girlfriend | name |

**Relationship Mentions (Provenance):**
| Fact | Source Type | Relationship ID |
|------|-------------|-----------------|
| Tyler is dating Girlfriend | `self_disclosed` | `fa7d178b-...` |

### Key Observations
- ✅ Relationship (DATING) correctly extracted from casual mention
- ✅ Source type correctly identified as `self_disclosed`
- ⚠️ "Girlfriend" extracted as entity name (could be enhanced to resolve to Casey)
- ⚠️ Technical concepts (app, memory system) not extracted as entities

---

## Summary Statistics

| Fixture | Entities | Relationships | Aliases | Mentions |
|---------|----------|---------------|---------|----------|
| identity-disclosure | 3 | 1 | 4 | 2 |
| job-change | 4 | 3 | 4 | 3 |
| social-relationship | 4 | 1 | 5 | 2 |
| gmail/work-thread | 3 | 3 | 3 | 3 |
| gmail/newsletter-sender | 7 | 6 | 7 | 7 |
| aix/personal-info | 11 | 10 | 11 | 12 |
| aix/project-discussion | 2 | 1 | 2 | 1 |
| **Total** | **34** | **25** | **36** | **30** |

## Source Type Distribution

| Source Type | Count | Examples |
|-------------|-------|----------|
| `self_disclosed` | 9 | Tyler's email, Tyler dating girlfriend |
| `mentioned` | 16 | Third-party facts from context |
| `inferred` | 5 | Customer relationships from invoices |

## Entity Type Distribution

| Type | Count |
|------|-------|
| Person | 17 |
| Company | 7 |
| Location | 7 |
| Project/Document | 3 |
| Event | 1 |

---

## Areas for Enhancement

1. **Entity Merging**: Casey ↔ Casexadams, Cloudflare ↔ Cloudflare, Inc.
2. **Literal Extraction**: Compensation (280k TC), account numbers
3. **Subject Line Parsing**: Jeff/Vlad from email subjects
4. **Anonymous Resolution**: "Girlfriend" → Casey via context
