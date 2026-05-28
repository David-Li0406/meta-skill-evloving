---
name: marketing-email
description: Create marketing emails and newsletters using your brand voice. Use when asked to write emails, newsletters, launch announcements, email sequences, nurture emails, or promotional content for email. Triggers on "email", "newsletter", "email sequence", "nurture".
---

# Marketing Email Creator

Create compelling marketing emails in your authentic brand voice.

## Before Writing

1. **Identify the email type**:
   - Newsletter (regular value delivery)
   - Launch announcement (course/product promotion)
   - Nurture sequence (relationship building)

2. **Run the rhetoric selector**:
   ```bash
   python shared/rhetoric_selector.py --type email_newsletter
   # or --type email_launch
   # or --type email_nurture
   ```

3. **Review context**:
   - [VOICE_GUIDE.md](../../config/VOICE_GUIDE.md)
   - [BUSINESS_CONTEXT.md](../../config/BUSINESS_CONTEXT.md)
   - [CONTENT_PILLARS.md](../../config/CONTENT_PILLARS.md)

## Email Anatomy

### Subject Line
- 4-7 words ideal
- Create curiosity or promise value
- Rhetorical devices work brilliantly here (antithesis, tricolon)
- Avoid spam triggers (FREE, URGENT, !!!)
- Test with: "Would I open this?"

**Subject line formulas**:
- Curiosity: "The thing nobody tells you about [X]"
- Benefit: "How to [achieve X] in [timeframe]"
- Story: "I almost [dramatic thing] until..."
- Direct: "[Specific thing] that changed my [result]"
- Antithesis: "[Old way] vs [new way]"

### Preview Text
- First 40-90 characters visible in inbox
- Complements (doesn't repeat) subject line
- Often the first sentence of your email

### Opening
- Don't waste the first line on "Hi [Name]"
- Start with something interesting
- Hook them immediately - they're deciding whether to keep reading

### Body
- Short paragraphs (2-3 sentences max)
- One idea per paragraph
- Use rhetorical devices for flow and emphasis
- Personal stories are your secret weapon
- Specifics > generalities (numbers, examples, real situations)

### CTA (Call to Action)
- ONE clear CTA per email
- Button or link, not both
- Action-oriented text ("Join the masterclass" not "Click here")
- Earned, not forced - comes after providing value

### Sign-off
- Keep it simple: Your name or "- [Name]"
- P.S. lines work for secondary CTAs or personal notes

## Templates

See templates folder:
- [Newsletter](templates/newsletter.md)
- [Launch Announcement](templates/launch-announcement.md)
- [Nurture Sequence](templates/nurture-sequence.md)

## Voice Reminders

From your [VOICE_GUIDE.md](../../config/VOICE_GUIDE.md):

### Do
- Write like you're emailing one person
- Share real stories and real numbers
- Be genuinely helpful before asking for anything
- Use "you" more than "I"
- Maintain your spelling conventions

### Don't
- Start with "I hope this email finds you well"
- Use "we" when you mean "I"
- Include multiple CTAs competing for attention
- Write walls of text without line breaks
- Sound like a marketing department

## Email Types Explained

### Newsletter
**Purpose**: Regular value delivery, staying top of mind
**Frequency**: Weekly or bi-weekly
**Mix**: Technical tip + industry observation + personal note
**CTA**: Soft (reply, share, optional product mention)

### Launch Announcement
**Purpose**: Promote a specific offering
**Frequency**: During launch windows only
**Structure**: Problem > Solution > Proof > Offer > Urgency
**CTA**: Direct (join, enrol, sign up)

### Nurture Sequence
**Purpose**: Build relationship over time with new subscribers
**Length**: 5-7 emails over 2-3 weeks
**Arc**: Welcome > Value > Story > More value > Soft pitch
**CTA**: Graduated (reply > free resource > learn more > offering)

## Quality Checklist

Before sending, verify:
- [ ] Subject line creates curiosity or promises clear value
- [ ] Opening line is interesting (not "Hi, I hope...")
- [ ] Paragraphs are short and scannable
- [ ] Voice is authentically yours (check against guide)
- [ ] At least one rhetorical device used naturally
- [ ] ONE clear CTA (or none if pure value email)
- [ ] CTA is earned (value delivered first)
- [ ] No spelling errors
- [ ] Read aloud - does it sound like a person?
