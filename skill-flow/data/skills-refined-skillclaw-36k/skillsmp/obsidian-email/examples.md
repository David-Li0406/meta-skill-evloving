# Email Chain Processing Examples

## Example 1: Basic Email Chain Processing

### Input File

```markdown
---
when: 2026-01-23
tags:
  - note
---
# Participants


# Summary



# Email Chain

From: Smith, John <john.smith@hpe.com>
Date: Monday, January 20, 2026 at 2:30 PM
To: Team <team@hpe.com>
Subject: Project Update

Hello team,

Just wanted to provide a quick update on the project status.

Thanks,
John

---

**From:** Johnson, Alice <alice.johnson@hpe.com>
**Sent:** Monday, January 20, 2026 3:45 PM
**To:** Smith, John <john.smith@hpe.com>
**Subject:** RE: Project Update

Thanks John,

Can you provide more details on the timeline?

Best,
Alice
```

### After Processing

```markdown
---
when: 2026-01-23
tags:
  - note
---
# Participants

- [[Smith, John|John Smith]]
- [[Johnson, Alice|Alice Johnson]]

# Summary

## Overview
Email thread regarding: Project Update

Thread contains 2 messages from 2 participants.

## Key Points
- Discussion involves multiple stakeholders across teams

## Action Items
- Review email chain for specific action items and deadlines
- Follow up on open issues discussed

## Context
See full email chain below for complete discussion details.


# Email Chain

[Same content as before]
```

### Created People Profiles

**File: `~/Documents/Obsidian/HPE/People/Smith, John.md`**
```markdown
---
tags:
  - person
---

# Smith, John

## Contact
- Email: john.smith@hpe.com

## Aliases
- [[Smith, John|John Smith]]
```

**File: `~/Documents/Obsidian/HPE/People/Johnson, Alice.md`**
```markdown
---
tags:
  - person
---

# Johnson, Alice

## Contact
- Email: alice.johnson@hpe.com

## Aliases
- [[Johnson, Alice|Alice Johnson]]
```

## Example 2: Email with Multiple Names and Tickets

### Input File

```markdown
---
when: 2026-01-23
tags:
  - note
---
# Participants


# Summary



# Email Chain

From: Vobbilisetty, Suresh <suresh.vobbilisetty@hpe.com>
Date: Friday, January 23, 2026 at 7:43 AM
To: Yun, Stella <xiaoyang.yun@hpe.com>
Subject: Re: DGTS Sustainability - OpsRamp

Stella - please check with the team on this.

We need an update by noon today regarding [[GLCP-322691]].

Thanks,
Suresh.

---

**From:** Yun, Stella <xiaoyang.yun@hpe.com>
**Sent:** Friday, January 23, 2026 8:15 AM
**To:** Vobbilisetty, Suresh <suresh.vobbilisetty@hpe.com>
**Subject:** RE: DGTS Sustainability - OpsRamp

Hi Suresh,

Working on it now. Will have update before the meeting.

Best,
Stella
```

### Processing Output

```
✓ Extracted 2 unique participants
  - Vobbilisetty, Suresh (suresh.vobbilisetty@hpe.com)
  - Yun, Stella (xiaoyang.yun@hpe.com)
✓ Updated 2 profiles with email addresses
✓ Updated Participants section
✓ Generated summary (4 sections)
✓ Updated 2026-01-23 - DGTS Sustainability.md
```

### After Processing

```markdown
---
when: 2026-01-23
tags:
  - note
---
# Participants

- [[Vobbilisetty, Suresh|Suresh Vobbilisetty]]
- [[Yun, Stella|Stella Yun]]

# Summary

## Overview
Email thread regarding: Re: DGTS Sustainability - OpsRamp

Thread contains 2 messages from 2 participants.

## Key Points
- Discussion involves multiple stakeholders across teams
- References tickets: [[GLCP-322691]]

## Action Items
- Review email chain for specific action items and deadlines
- Follow up on open issues discussed

## Context
See full email chain below for complete discussion details.


# Email Chain

[Same content as before]
```

## Example 3: Long Email Chain with Multiple Participants

### Command Line Usage

```bash
# Find email notes
find ~/Documents/Obsidian/HPE/Notes -iname "*ops*ramp*email*.md"

# Process the email
python ~/skills/obsidian-email/scripts/process_email.py \
  ~/Documents/Obsidian/HPE/Notes/2026-01-23\ -\ Ops\ Ramp\ Issues\ Email.md
```

### Output

```
✓ Extracted 5 unique participants
  - Vobbilisetty, Suresh (suresh.vobbilisetty@hpe.com)
  - Sadananda, Ravi Kiran Srirangam (ravikiransrirangam.sadananda@hpe.com)
  - Daniel, Binu (binu.daniel@hpe.com)
  - Vanteru, Bhanu (bhanu.vanteru@hpe.com)
  - Yun, Stella (xiaoyang.yun@hpe.com)
✓ Created 4 new People profiles
✓ Updated 1 profiles with email addresses
✓ Updated Participants section
✓ Generated summary (4 sections)
✓ Updated 2026-01-23 - Ops Ramp Issues Email.md
```

## Example 4: Handling Middle Names

### Input From Header

```
From: Van Der Berg, Jan Willem <jan.vandeberg@hpe.com>
```

### Generated Links

```markdown
- [[Van Der Berg, Jan Willem|Jan Willem Van Der Berg]]
```

### Profile Created

```markdown
---
tags:
  - person
---

# Van Der Berg, Jan Willem

## Contact
- Email: jan.vandeberg@hpe.com

## Aliases
- [[Van Der Berg, Jan Willem|Jan Willem Van Der Berg]]
```

## Example 5: Mixed Email Format (Outlook + Plain)

### Input Email Chain

```markdown
# Email Chain

From: Lee, Sarah <sarah.lee@hpe.com>
Date: Wednesday, January 15, 2026 at 9:00 AM
To: Team <team@hpe.com>

Initial message here.

---

**From:** Chen, Michael <michael.chen@hpe.com>
**Sent:** Wednesday, January 15, 2026 10:30 AM
**To:** Lee, Sarah <sarah.lee@hpe.com>

Reply message here.
```

### Result

Both formats are correctly parsed:
```
✓ Extracted 2 unique participants
  - Lee, Sarah (sarah.lee@hpe.com)
  - Chen, Michael (michael.chen@hpe.com)
```

## Example 6: Adding Email to Existing Profile

If profile already exists but without email:

### Existing Profile
```markdown
---
tags:
  - person
---

# Smith, John

## Aliases
- [[Smith, John|John Smith]]
```

### After Processing
```markdown
---
tags:
  - person
---

# Smith, John

## Contact
- Email: john.smith@hpe.com

## Aliases
- [[Smith, John|John Smith]]
```

### Output
```
✓ Extracted 1 unique participants
  - Smith, John (john.smith@hpe.com)
✓ Updated 1 profiles with email addresses
✓ Updated Participants section
✓ Generated summary (4 sections)
```
