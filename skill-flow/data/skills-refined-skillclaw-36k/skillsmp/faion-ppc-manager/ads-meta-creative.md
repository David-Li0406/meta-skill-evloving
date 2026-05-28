---
id: meta-creative
name: "Meta Creative Best Practices"
domain: ADS
skill: faion-marketing-manager
category: "advertising"
---

# Meta Creative Best Practices

## Metadata

| Field | Value |
|-------|-------|
| **ID** | meta-creative |
| **Name** | Meta Creative Best Practices |
| **Category** | Ads API |
| **Difficulty** | Intermediate |
| **Agent** | faion-ads-agent |
| **Related** | meta-campaign-setup, meta-targeting, copywriting-fundamentals |

---

## Problem

Your targeting is perfect but ads don't convert. People scroll past without stopping. Your click-through rate is below 1%. Creative is the most important factor in ad performance, yet most spend 90% of their time on targeting.

Great creative stops the scroll, communicates value, and drives action in seconds.

---

## Framework

Ad creative follows the AIDA pattern:

```
ATTENTION -> Stop the scroll (visual + hook)
INTEREST  -> Engage them (relevance)
DESIRE    -> Create want (benefits, proof)
ACTION    -> Drive click (CTA)
```

### Step 1: Understand Ad Formats

**Format comparison:**

| Format | Best For | Specs |
|--------|----------|-------|
| **Static image** | Simple messages | 1080x1080 (1:1) or 1080x1920 (9:16) |
| **Video** | Storytelling, demos | 15-30 sec, vertical or square |
| **Carousel** | Multiple products/benefits | 2-10 images, 1080x1080 |
| **Collection** | E-commerce | Instant Experience |
| **Stories/Reels** | Full-screen immersion | 1080x1920, 15 sec max |

**Format selection:**
- Start with static images (fastest to test)
- Add video once you find winning angles
- Use carousel for feature showcases

### Step 2: Create Scroll-Stopping Visuals

**Visual hierarchy:**
1. Hero image/video (main focus)
2. Key text (headline overlay)
3. Branding (subtle, not dominant)

**What works:**
- Faces with emotion
- Before/after contrasts
- Product in action
- Bold, contrasting colors
- Text overlays (but not too much)
- Motion in first 3 seconds (video)

**What doesn't work:**
- Stock photos (obviously fake)
- Too much text
- Busy compositions
- Low contrast
- Small products/faces

**The 3-second rule:**
- Video must hook in 3 seconds
- Image must communicate in 3 seconds
- If it doesn't stop scroll, nothing else matters

### Step 3: Write Compelling Copy

**Copy structure:**

| Element | Character Limit | Best Practice |
|---------|-----------------|---------------|
| Primary text | ~125 shown (more behind "See more") | Hook first, details second |
| Headline | ~40 | Benefit-focused, clear |
| Description | ~30 | Optional, supports headline |

**Hook formulas:**
```
Question hook:
"Tired of [problem]?"

Bold claim:
"We increased [metric] by 400%"

Curiosity:
"This simple change doubled our [result]"

Social proof:
"10,000+ [audience] are using this"

Direct benefit:
"Get [outcome] in [timeframe]"
```

**Primary text formula:**
```
[Hook - stop them]

[Pain point - empathize]

[Solution - introduce product]

[Benefit 1]
[Benefit 2]
[Benefit 3]

[Social proof]

[CTA]
```

### Step 4: Design for Placements

**Placement optimization:**

| Placement | Specs | Tips |
|-----------|-------|------|
| Feed | 1:1 or 4:5 | Can handle more text |
| Stories | 9:16 | Full screen, fast-paced |
| Reels | 9:16 | Native-looking, entertaining |
| Right column | 1:1 | Desktop only, simple |
| Search | 1:1 | Intent-based, direct |

**Asset requirements:**
- Create both 1:1 and 9:16 versions
- Use Advantage+ creative to auto-optimize
- Or manually select placements per format

### Step 5: Test Creative Systematically

**Testing framework:**
1. Test hooks first (biggest impact)
2. Then test visuals
3. Then test copy details
4. Then test formats

**Testing structure:**
```
Ad Set: [Audience]
├── Ad 1: Hook A + Visual A
├── Ad 2: Hook B + Visual A
├── Ad 3: Hook C + Visual A
├── Ad 4: Hook A + Visual B
└── Ad 5: Hook A + Visual C

Isolate variables to learn what works
```

**Minimum spend per creative:**
- $20-50 before judging
- 1,000+ impressions
- Statistical significance needed

### Step 6: Avoid Creative Fatigue

**Signs of fatigue:**
- Declining CTR over time
- Rising CPM
- Decreasing conversion rate
- Same audience, worse results

**Prevention:**
- Refresh creatives every 2-4 weeks
- Have 5-10 variations ready
- Iterate on winners (don't start from scratch)
- Test new angles continuously

---

## Templates

### Image Ad Spec Sheet

```markdown
## [Ad Name]

### Visual
- Format: Image
- Size: 1080x1080 (1:1)
- Elements:
  - [ ] Main subject
  - [ ] Text overlay: [text]
  - [ ] Logo placement
  - [ ] Color scheme

### Copy
**Primary text:**
[Hook]

[Body]

[CTA]

**Headline:** [40 chars]
**Description:** [30 chars]
**CTA button:** [Learn More / Sign Up / Shop Now]

### Tracking
- UTM: [parameters]
```

### Video Ad Script

```markdown
## [Video Name] - [Length] sec

### Scene 1 (0-3 sec) - HOOK
[Visual]: [What's on screen]
[Audio]: [What's said/heard]
[Text overlay]: [On-screen text]

### Scene 2 (3-10 sec) - PROBLEM
[Visual]:
[Audio]:
[Text overlay]:

### Scene 3 (10-20 sec) - SOLUTION
[Visual]:
[Audio]:
[Text overlay]:

### Scene 4 (20-25 sec) - PROOF
[Visual]:
[Audio]:
[Text overlay]:

### Scene 5 (25-30 sec) - CTA
[Visual]:
[Audio]:
[Text overlay]:

### Production Notes
- [ ] Captions required
- [ ] Vertical (9:16) version needed
- [ ] Square (1:1) version needed
```

---

## Examples

### Before/After Copy

**Before (feature-focused):**
```
Our software uses AI to analyze your marketing data.
Features include: dashboard, reports, integrations.
Sign up today!
```

**After (benefit-focused):**
```
Stop guessing which marketing works.

You're spending $10K+ on ads. But which ones actually drive sales?

[Product] shows you in 60 seconds:
- Which campaigns are profitable
- Where you're wasting money
- What to do next

10,000+ marketers use it daily.

Start free → (link)
```

### Video Hook Examples

**Product demo:**
```
0-3s: "Watch how I do [outcome] in [time]"
[Show result first, then how]
```

**Testimonial:**
```
0-3s: Customer face, strong statement
"I made $50K using this one strategy"
```

**Problem/solution:**
```
0-3s: Show the frustrating problem
"When your ads aren't working..."
```

---

## Implementation Checklist

### Preparation
- [ ] Define value proposition
- [ ] List 5 hooks to test
- [ ] Gather visual assets
- [ ] Write copy variations

### Production
- [ ] Create 1:1 and 9:16 versions
- [ ] Design 3-5 image variations
- [ ] Script and produce 2-3 videos
- [ ] Add text overlays/captions

### Setup
- [ ] Upload to Ads Manager
- [ ] Set naming conventions
- [ ] Add tracking parameters
- [ ] Preview all placements

### Testing
- [ ] Launch with multiple creatives
- [ ] Monitor for 3-5 days
- [ ] Identify winners
- [ ] Iterate on what works

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Stock photos | Looks like an ad | Use real photos/UGC |
| Too much text | Won't stop scroll | One message, big |
| No hook | Scrolled past | Hook in first line/3 sec |
| Feature-focused | Doesn't resonate | Lead with benefits |
| No CTA | No action taken | Clear, specific CTA |
| One creative | No learning | 3-5 minimum |

---

## Creative Performance Benchmarks

| Metric | Poor | Average | Good |
|--------|------|---------|------|
| CTR (Feed) | <0.5% | 0.8% | 1.5%+ |
| CTR (Stories) | <0.3% | 0.5% | 1%+ |
| Video view (3s) | <20% | 30% | 50%+ |
| Video view (75%) | <5% | 10% | 20%+ |
| Thumb-stop rate | <10% | 15% | 25%+ |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Design | Canva, Figma, Adobe Express |
| Video | CapCut, InShot, Premiere |
| UGC sourcing | Billo, Insense |
| Inspiration | Meta Ad Library |
| AI generation | Midjourney, DALL-E |

---

## Related Methodologies

- **meta-campaign-setup:** Meta Campaign Setup
- **meta-targeting:** Meta Targeting
- **copywriting-fundamentals:** Copywriting Fundamentals
- **ab-testing-ads:** A/B Testing Ads

---

*Methodology: meta-creative | Ads API | faion-ads-agent*
