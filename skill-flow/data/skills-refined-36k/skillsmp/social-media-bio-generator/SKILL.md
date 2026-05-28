---
name: social-media-bio-generator
description: Generates multiple high-converting bio options for LinkedIn, X (Twitter), and Instagram based on user context. Creates platform-optimized bios with proper character limits, formatting, and conversion focus. Use when user mentions "write my bio", "LinkedIn headline", "Twitter bio", "Instagram bio", or wants to optimize social media profiles.
---

# Social Media Bio Generator

**Purpose:** Generate multiple high-converting bio options for LinkedIn, X (Twitter), and Instagram that attract the right audience and drive profile actions.

## When to Activate

Use this skill when:
- User asks to write or optimize their social media bio
- User mentions "LinkedIn headline", "Twitter bio", or "Instagram bio"
- User wants to update their professional profile descriptions
- User says "help me with my social profiles"
- User needs bios for multiple platforms

## Core Principles

1. **No Fabrication**: Do not create personal stories, anecdotes, experiences, or achievements unless explicitly provided by the user
2. **Evidence-Based**: All claims, metrics, and credentials must come directly from user input
3. **Multiple Options**: Generate 3-5 bio variations per platform to provide choice
4. **Platform Optimization**: Strictly adhere to each platform's character limits and best practices
5. **Conversion Focus**: Every bio should clearly communicate value and encourage profile actions

## Workflow

### Step 0: Load Context Profiles

Before starting, load all context profiles in /context.

If context profiles exist, use them for voice, business details, and target audience information.

If profiles don't exist, ask user for information directly (see Step 1).

### Step 1: Gather Additional Information

**Note:** If context profiles loaded, you have most information. Ask only for platform-specific details.

**Ask the user:**

**If context profiles loaded:**
```
I've loaded your context profiles (voice DNA, business profile, and ICP). I have your core information!

Which platforms do you need bios for?
- LinkedIn (headline + about section)
- X (Twitter)
- Instagram

Just need to know:
1. **Primary goal** for these profiles? (leads, opportunities, brand awareness, etc.)
2. **Call-to-action preference**? (newsletter, website, booking, etc.)
3. **Any specific tone adjustments** for these platforms? (or use voice DNA defaults)

That's all - I'll create platform-optimized bios using your context!
```

**If no context profiles:**
```
I'll help you create high-converting bios optimized for LinkedIn, X (Twitter), and Instagram.

Which platforms do you need bios for? (Select all that apply)
- LinkedIn (headline + about section)
- X (Twitter)
- Instagram

To create effective bios, please provide:

**Essential Information:**
1. Current role/title
2. Target audience (who do you want to attract?)
3. What you do / expertise areas
4. Unique value proposition (what makes you different?)
5. Primary goal for your profile (leads, job opportunities, brand awareness, etc.)

**Helpful Details:**
6. Key achievements with specific metrics (revenue, followers, clients, etc.)
7. Credentials or affiliations
8. Current projects or offerings
9. Topics you're known for
10. Call-to-action preference (newsletter, website, booking, etc.)
11. Preferred tone (professional, casual, bold, etc.)

Provide as much detail as you can - the more context, the better the bios!
```

### Step 2: Generate Platform-Specific Bios

Generate 3-5 variations for each requested platform following the specifications below.

## LinkedIn Bios

### Headline Section (220 characters max)

**Structure Formula**: [What You Do] | [Who You Help] | [Unique Value/Differentiator]

**Create 3-5 headline variations:**

**Variation Approaches:**
- **Variation 1**: Focus on helping specific audience achieve measurable outcome
- **Variation 2**: Lead with biggest achievement or credential
- **Variation 3**: Emphasize unique methodology or approach
- **Variation 4**: Highlight transformation or journey (if provided)
- **Variation 5**: Focus on mission/vision for industry change

**Requirements:**
- Start with "I help [target audience] achieve [specific outcome]" formula (when appropriate)
- Include ONE credibility marker (role, achievement, or metric from user data)
- Add 2-3 topic hashtags or focus areas
- Write for search optimization with relevant keywords
- **Avoid**: Job title only, vague descriptions, clever over clear

**Example Format:**
```
I help [audience] achieve [outcome] | [Credential/Role] | Topics: [keyword1], [keyword2], [keyword3]
```

### About/Summary Section (2,600 characters max)

**Structure:**
1. **Opening Hook** (1-2 sentences)
   - Compelling mission statement or surprising insight
   - Based on user's unique angle

2. **Background** (2-3 sentences)
   - Professional journey highlights
   - Unique approach or methodology
   - Use only information user provided

3. **Social Proof** (2-4 sentences)
   - Specific achievements from user data
   - Client results or impact metrics
   - Brand associations or credentials

4. **Current Focus** (2-3 sentences)
   - What they're building/doing now
   - Who they serve and how

5. **Call-to-Action** (1-2 sentences)
   - Aligned with their stated goals
   - Clear next step for connections

**Tone**: Conversational while maintaining professionalism

## X (Twitter) Bios

### Structure Requirements (160 characters STRICT limit)

**Essential Components:**
- Memorable descriptor or "moniker" (2-5 words)
- Current role/project in action-oriented language
- What followers gain (topics, value, promise)
- ONE proof point if space permits
- Strategic emoji usage (1-3 max)

**Format Options:**
- Single line with | or • separators
- Multi-line with line breaks
- Emoji-structured bullets

**Create 3-5 Twitter bio variations:**

**Variation Approaches:**
- **Variation 1**: Moniker + Mission + Topics format
- **Variation 2**: Achievement-first with follower benefit
- **Variation 3**: Action-oriented "Building/Creating X" focus
- **Variation 4**: Topic expertise with credibility marker
- **Variation 5**: Minimalist high-impact statement

**Example Formats:**
```
[Moniker] | [What I do] | [Topics] | [Proof point]

[Role] • [Mission]
[Topics] • [Value delivered]

🚀 [Achievement]
Sharing [topics] for [audience]
```

**Critical**: Count characters carefully. 160 is the hard limit.

## Instagram Bios

### Structure Requirements (150 characters STRICT limit)

**Essential Components:**
- Clear identity/title with USP
- Benefit or transformation offered
- Call-to-action with directional emoji (👇)
- Strategic line breaks for scannability
- 3-5 emojis maximum for visual hierarchy

**Formatting Rules:**
- Use line breaks after each key element
- Lead emoji for each line where appropriate
- Keywords in plain text (not hashtags)
- CTA as final line pointing to link

**Create 3-5 Instagram bio variations:**

**Variation Approaches:**
- **Variation 1**: Title + Big Number + CTA structure
- **Variation 2**: Mission-first with credibility marker
- **Variation 3**: Benefit-focused with personal touch
- **Variation 4**: Expertise + Location + Link focus
- **Variation 5**: Transformation promise with proof

**Example Formats:**
```
[Emoji] [Identity/Title]
[Emoji] [Benefit/Transformation]
[Emoji] [Credibility marker]
👇 [CTA text]
```

**Critical**: Count characters carefully. 150 is the hard limit.

## Content Generation Guidelines

### Optimization Techniques

1. **Keyword Integration**: Naturally incorporate industry terms for search
2. **Social Proof**: Use only verified metrics/achievements from user input
3. **Clarity Over Cleverness**: Ensure value is immediately apparent
4. **Audience Language**: Mirror terminology used by target demographic
5. **Action Orientation**: Use present-tense, dynamic verbs

### Information Gap Handling

**If user provides limited information:**
- Request specific details needed
- Provide examples to clarify what you need
- Create template-style bios with [brackets] for them to fill
- Explain why each piece of information matters

**Never create fictional:**
- Achievements or metrics
- Client testimonials
- Credentials or affiliations
- Personal stories

## Output Format

**Present bios clearly labeled by platform:**

```
# Social Media Bio Options

Based on your context: [brief summary of what you're working with]

---

## LinkedIn Bio Options

### Option 1: [Descriptive Label - e.g., "Achievement-First"]
**Headline** (XXX/220 characters):
[Headline text]

**About Section**:
[Full about section with proper formatting and line breaks]

### Option 2: [Descriptive Label]
[Continue pattern for 3-5 options...]

---

## X (Twitter) Bio Options

### Option 1: [Descriptive Label - e.g., "Moniker + Mission"]
[Bio text]

Character count: XX/160

### Option 2: [Descriptive Label]
[Continue pattern for 3-5 options...]

---

## Instagram Bio Options

### Option 1: [Descriptive Label - e.g., "Title + Number + CTA"]
[Bio with line breaks as they would appear]
[Second line]
[Third line]
👇 [CTA]

Character count: XX/150

### Option 2: [Descriptive Label]
[Continue pattern for 3-5 options...]

---

## Recommendations

**LinkedIn**: I recommend Option [X] because [reasoning based on their goals]
**Twitter**: I recommend Option [X] because [reasoning]
**Instagram**: I recommend Option [X] because [reasoning]

**Next Steps**: [Suggestions for implementation, testing, or additional optimization]
```

## Quality Checks

Before presenting bios:
- [ ] All character counts are within platform limits
- [ ] No fabricated achievements or credentials
- [ ] Clear value proposition in each version
- [ ] Platform-appropriate formatting
- [ ] CTAs align with user's stated goals
- [ ] Consistent facts across all variations
- [ ] Keywords naturally integrated
- [ ] Specific and measurable (not vague)
- [ ] Avoid generic phrases like "passionate about" or "love what I do"

## Example Interaction

**User:** "I need bios for LinkedIn and Twitter. I'm a content strategist who helps B2B companies with thought leadership. I've worked with 50+ companies and my content has generated 10M+ views."

**Claude (using this skill):**
```
Great! I'll create optimized bios for LinkedIn and Twitter.

A few more questions to make these perfect:

1. Who's your target audience? (e.g., "B2B marketing leaders", "SaaS founders")
2. What's your unique approach or methodology?
3. What do you want people to do? (connect, visit website, book call, etc.)
4. Any specific credentials or notable clients you want to mention?
5. Preferred tone? (authoritative, approachable, bold, etc.)

Once I have these details, I'll create 3-5 options for each platform!
```

## Best Practices

**For all platforms:**
- Lead with value, not job title
- Use specifics over generalities
- Show results, not just activities
- Make it scannable and clear
- Include clear call-to-action
- Test multiple variations

**LinkedIn specific:**
- Optimize for search keywords
- Use first-person perspective in About
- Include links where relevant
- Update regularly based on focus changes

**Twitter specific:**
- Every character counts - be ruthless
- Use emojis strategically for visual breaks
- Consider what will stand out in timeline
- Update as your focus evolves

**Instagram specific:**
- Visual hierarchy matters - use line breaks
- Emoji at start of line creates structure
- Direct to link in bio with clear CTA
- Keep it simple and scannable

---

**Remember:** Your bio is often the first impression. Make it clear, compelling, and conversion-focused. Test different versions and update based on what resonates with your target audience.
