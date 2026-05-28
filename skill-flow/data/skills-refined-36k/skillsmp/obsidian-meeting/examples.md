# Meeting Note Examples

## Example 1: Complete Processed Meeting (SIC-PCE Syncup)

This example shows a fully processed meeting note with all elements:
- YAML frontmatter
- Attendee list with linked profiles and counts
- Subject line
- Structured meeting notes with summary
- Clean formatted transcript

---

## Full Meeting Note

```markdown
---
when: 2026-01-08
tags:
  - meeting
---
# Attendees

## In Meeting (6)
- [[Willmschen, Royce|Royce Willmschen]]
- [[Colton, Will|Will Colton]]
- [[Hirve, Sayali|Sayali Hirve]]
- [[Mohammed, Shaji|Shaji Mohammed]]
- [[Pahwa, Kashish|Kashish Pahwa]]
- [[Piddington, Ila|Ila Piddington]]

# Subject
- PCE Data Collection and Site/Location Implementation

# Notes

## Meeting Purpose
SIC-PCE Syncup to discuss progress on fetching PCE (Private Cloud Enterprise) power data and implementing site/location data for Sustainability Insight Center.

## Key Discussion Points

### PCE Data Service Status
- **Current state**: Service for fetching PCE power data was reviewed by engineering team ~1 month ago
- **Recent work**: Service has been hardened and made more reliable after initial fragility concerns
- **Technical issues**: Resolved collector service issues that were affecting all collectors
- **Status**: Out for re-review by engineering team to verify fixes

### PDU Data Implementation
- **Decision**: Using PDU (Power Distribution Unit) data as primary data source
- **Technical detail**: PDU data doesn't have a "power" tag (ironic given the purpose)
- **Status**: Working in local testing, awaiting engineering review

### Site/Location Data Challenge
- **Current state**: Explored existing PCE site data across all customers
- **Key finding**: Only 3 customers have useful site data with details filled in
- **Problem**: Sites only require a name field - most have no location details
- **Available data**: 3 customers have "United States" as country - enough to proceed
- **Impact**: Without proper location data, power data accuracy is limited and some sites show as "whole globe"

### Implementation Approach
- **Site-PDU linkage**: Figured out how to link PDU data to sites (not straightforward)
- **Technical challenge**: Must get site and list every device that site has - heavier bandwidth than ideal
- **Status**: Technically thought through and tested locally, now implementing into service
- **Next step**: Create GreenLake location for each site with location data, associate with location ID

### Team Context
- Will Colton: Leading the PCE data collection implementation
- Kashish Pahwa: Product team member asking clarifying questions
- Royce Willmschen: SIC Engineering Manager providing context
- Sayali Hirve: Team member (started transcription)

### Important Notes
- Recording listeners should be aware: Better location data in PCE sites will yield more accurate power consumption data
- Work is in progress on linking PCE sites to GreenLake locations via APIs



## Transcript

**[[Colton, Will|Will Colton]]** 0:03

So I'll give a general overview. Basically we had a the service that's fetching the the PC data is this. The basic structure of the service was reviewed about a maybe a month ago by the engineering team.

And had some things they want it cleaned up. It sort of worked, but it was like a little fragile and so it's been hardened and made more into like a real reliable service, that version of the service. Then there were some technical issues that were unrelated to the service that were basically breaking all of the collector services. So I spent. I had a sort of a long foray where I was.

Fixing that stuff, but now it's back to working and so it's out for a re review by the engineering team to make sure that everything was fixed up as expected and that it looks good as well as in the meantime we had made the decision to use the PDU data as the primary data. So I switched from using just grabbing everything that said power.

To specifically the PDU data, which ironically does not have A tag of power and so as as as was requested. So that should now be working and or is now working in my local testing but is out for review. So in the meantime.

I have been working on site slash location data. I explored the existing data for sites across all of all of the PCE data and they really only have 3 customers with any site data. I take that back they all they have site data for all.

They have 3 customers with any useful site data. They only have 3 customers that have anything entered into the details for sites. So sites can don't. Sites are required only to have a name. They basically don't have any required.

Fields and so most of the sites are just blank across all of PCE. We have 3 customers that have just the country of the United States and that's it as the only detail. Now the United States is sort of enough for us to get going, so I'm moving forward with.

With our plan of adding location data using the sites, but just for everybody here and for anybody who listens to recording, be aware that it'll be. It'll definitely be better if people actually fill in the location data for those sites, we'll get more accurate power data.

And also it'll actually we'll get anything other than the whole globe for the sites that actually don't have location data at all. So that is Kashish, you wanna? Yeah, you can interrupt. I'm not a it's not a yeah, not a prepared presentation.

**[[Pahwa, Kashish|Kashish Pahwa]]** 2:51

Complete your thought. I'll you can complete your thought. I I just had a couple of questions.

**[[Colton, Will|Will Colton]]** 2:54

OK, so that's pretty much it. So now I'm work in progress. So I figured out that. So now I'm I figured out how to link the PDEPC, the PDU data to a site, which is is not a straightforward. It basically works in the direction I wouldn't like. You have to get like get a site and list every single device that site has ever.

So it's just going to be a lot. It's going to be a little heavier bandwidth wise than I'd like, but I think it should work fine and and so that that has been technically thought at thought through and tested locally and now I'm actually implementing it into the service itself. The next step will be once I have that site data and the PDU data coordinated actually creating.

A GreenLake location for a site for each site that actually has location data in order to be using the GreenLake APIs and then and then obviously associating that and then that will be sent along with the location ID, the GLP.

Location ID that I've created out of the PCE sites will be sent to SIC so that SIC actually has as an associate correctly associated location and that we get all the benefits of that once that's done. So there's so there's definitely still still some steps left.

But it made good progress.

Uh, now I'm dumb, I thought.

## Media


# Take Aways
- 

# Actions
- 


## Transcript

**[[Colton, Will|Will Colton]]** 0:03

So I'll give a general overview. Basically we had a the service that's fetching the the PC data is this. The basic structure of the service was reviewed about a maybe a month ago by the engineering team.

And had some things they want it cleaned up. It sort of worked, but it was like a little fragile and so it's been hardened and made more into like a real reliable service, that version of the service. Then there were some technical issues that were unrelated to the service that were basically breaking all of the collector services. So I spent. I had a sort of a long foray where I was.

**[[Pahwa, Kashish|Kashish Pahwa]]** 2:51

Complete your thought. I'll you can complete your thought. I I just had a couple of questions.

**[[Colton, Will|Will Colton]]** 2:54

OK, so that's pretty much it. So now I'm work in progress. So I figured out that. So now I'm I figured out how to link the PDEPC, the PDU data to a site, which is is not a straightforward. It basically works in the direction I wouldn't like. You have to get like get a site and list every single device that site has ever.

**[[Willmschen, Royce|Royce Willmschen]]** 4:15

It will, I kind of want to talk through the precedence here then. So every measurement that we get from OPS ramp can potentially have a site associated with it, is that correct?
```

---

## Key Elements Demonstrated

### 1. YAML Frontmatter
```yaml
---
when: 2026-01-08
tags:
  - meeting
---
```

### 2. Attendee List
- Section header with count: `## In Meeting (6)`
- Linked profiles: `[[Last, First|First Last]]`
- No image references (removed after extraction)

### 3. Subject Line
Single line describing the meeting topic

### 4. Structured Notes
- `## Meeting Purpose` - Brief overview
- `### Topic Areas` - Organized by discussion topic
- **Bold keywords** for scanability
- Bullet points for details

### 5. Clean Transcript
- Section header: `## Transcript`
- Speaker format: `**[[Last, First|First Last]]** timestamp`
- Blank lines between speakers
- Multi-paragraph content preserved
- No images, metadata, or unwanted formatting

---

## Example 2: Attendee List Best Practices

```markdown
# Attendees

## In Meeting (9)
- [[Tronkowski, Kevin|Kevin Tronkowski]]
- [[Bennett, Ryan|Ryan Bennett]]
- [[Colton, Will|Will Colton]]
- [[Griffin, Drew|Drew Griffin]]
- [[Guo, Chris|Chris Guo]]
- [[Kumar, Yogesh|Yogesh Kumar]]
- [[Oh, Kyu|Kyu Oh]]
- [[Ricks, Darra|Darra Ricks]]
- [[Westfall, Thomas|Thomas Westfall]]

## Others Invited (5)
- [[Willmschen, Royce|Royce Willmschen]]
- [[Piddington, Ila|Ila Piddington]]
- [[Pomata, Alex|Alex Pomata]]
- [[Lynch, David|David Lynch]]
- [[Zhou, Shikuang|Shikuang Zhou]]
```

**Note:**
- Include count in section header
- Alphabetical order within sections not required
- Extract order from Teams screenshot preserved
- Each person gets their own People profile in `~/Documents/Obsidian/HPE/People/`

---

## Example 3: Meeting Summary Structure

```markdown
# Notes

## Meeting Purpose
Brief 1-2 sentence overview of the meeting topic and context.

## Key Discussion Points

### Topic Area 1
- **Current state**: Description of what exists now
- **Requirements**: What's needed or requested
- **Proposed solution**: Approach discussed
- **Status**: Current progress or decisions made

### Topic Area 2
- **Challenge**: Problem being addressed
- **Impact**: Consequences or implications
- **Next steps**: Follow-up actions

### Team Context
- Key stakeholders and their roles
- Relevant organizational information
- Background details

### Follow-up Plans
- Action items with owners
- Timeline commitments
- Dependencies or blockers noted
```

---

## Example 4: People Profile

Location: `~/Documents/Obsidian/HPE/People/Pahwa, Kashish.md`

```markdown
---
aliases:
  - Kashish Pahwa
tags:
  - People
---
```

**Profile structure:**
- Filename: `Last, First.md`
- Alias: `First Last` (for natural linking)
- Tag: `People` (for filtering)
- Content: Additional notes can be added below frontmatter

---

## Example 5: Augmenting Existing Summary (Magenta Standup Pattern)

This example shows how to handle meetings where summary sections already exist from Teams Copilot or manual notes.

### Before Processing

Meeting has existing summary sections but needs transcript cleanup and augmentation:

```markdown
---
when: 2026-01-12
tags:
  - meeting
---

# Decisions

- Enable facilitator agent for meeting recording.
- Merge secret scanning feature.

# Open questions

- Agreement needed on CXL cluster usage for forecasting.

# Agenda

Goal: Discuss and confirm the use of the facilitator agent.

# Meeting notes

### Meeting tools and automation

- Kevin described using Copilot to format meeting notes.
- Ila confirmed that the facilitator agent is now enabled.

## Transcript

[Raw Teams transcript with images and metadata...]
```

### After Processing

Existing sections are augmented with additional details from transcript analysis:

```markdown
---
when: 2026-01-12
tags:
  - meeting
---

# Decisions

- Enable facilitator agent for meeting recording and automated notes.
- Merge secret scanning feature and use Copilot for repo integration.
- Create separate story for secret scanning in all repos.
- Test agent-side work and coordinate for further development.
- Submit I18N header PR and hold review until implementation is ready.
- Follow up on OPS Ramp team setup and collaboration.
- Move QA maintenance story to 'done' after optimizations.
- Reach out to build packs team for Java 25 JVM image support.
- Assign Shiquang to agent work, Alex to provide guidance.

# Open questions

- Agreement needed on CXL cluster usage for forecasting.
- Resolve ML pipeline build failures due to runner disk space.
- Clarify team assignment and board tracking for OPS Ramp work.
- Investigate separating user input from prompts to pass Amazon guardrails.
- Analyze prompt aspects that trigger Amazon guardrails.
- Decide on architectural approach for guardrail checks.

# Agenda

Goal: Discuss and confirm the use of the facilitator agent for meeting recording and note-taking, and review project updates and code changes.

# Meeting notes

### Meeting tools and automation

- Kevin described using Copilot to format meeting notes and enable quick search in Obsidian
- Ila confirmed that the facilitator agent is now enabled to record meetings, provide transcripts, attendance, notes, and recaps
- Ila asked participants to confirm they are comfortable with meetings being recorded and the facilitator agent being used

### Security automation

- Will confirmed that the changes based on Ryan's feedback have been implemented and successfully tested, and the secret scanning job received final approval from Kevin.

### Forecasting updates

- Kyu relayed the forecasting update to the green and magenta teams and noted ongoing discussions about using the CXL cluster
- Kyu reported that the ML forecasting PR checks are failing due to build space issues, and Thomas is working on adjustments to resolve this

### Project progress

- Yogesh completed the worker side of their assigned task and began work on the agent side, planning to test and submit a PR soon

### Testing and QA

- Darra merged the GLCP auth and JS changes, reducing test run times from 4 hours to 30 minutes and resolving many app launch and login test failures.

### System upgrades

- Kevin updated the backend template and CCS event engine to Java 25, Gradle 9.2.1, and Spring Boot 4.0, and deployed the event engine as a native image.

### Task assignment

- Royce suggested that Shikuang coordinate with Alex to pick up the agent work item at the top of the list due to Alex's environment issues.

### Project collaboration

- Alex explained that OPS Ramp requested UI work, and Stella discussed Alex being temporarily assigned to their team for this project

### System integration challenges

- Alex described the need to pre-screen user requests with Amazon guardrails before processing them with their own system, due to strict guardrail restrictions that cause failures in their query ranking process
- Alex explained that attempts to enable Amazon guardrails caused all tests to fail due to strict restrictions, especially with prompt injection detection and ethical constraints.
- Alex described that the Genie team addressed similar guardrail issues by splitting user messages and using a two-step process to pass guardrails before further processing.
- Alex and Shikuang discussed that certain prompts, such as comparing two brands, triggered Amazon's ethical guardrails, preventing intended functionality.
- Alex explained that Amazon's ethical guardrails restrict certain queries, such as product comparisons and health-related questions, to prevent market manipulation and misinformation.

## Transcript

[Cleaned transcript with no images or metadata]
```

### Key Points in Augmentation

1. **Existing items preserved**: Original decisions and questions remain
2. **New items added**: Additional decisions and questions extracted from transcript
3. **Details enhanced**: Brief notes expanded with context from transcript
4. **New subsections added**: `### System integration challenges` was not in original
5. **Agenda enhanced**: More detail added while preserving original intent
6. **Structure maintained**: Uses existing section format (`# Decisions`, `# Open questions`, etc.)
7. **Transcript cleaned**: Images and metadata removed, speakers formatted

---

## Example 6: Downloaded Transcript Format

This example shows the **downloaded/exported Teams transcript format** which differs from direct paste.

### Raw Downloaded Transcript (Before Cleaning)

```markdown
## Transcript

**Green and Magenta Design Discussion-20260113_133528-Meeting Recording**

January 13, 2026, 6:35PM

1h 16m 5s

![](file:////Users/kevin/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image002.jpg)**Bennett, Ryan** started transcription

![](file:////Users/kevin/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image004.jpg)**Bennett, Ryan**   0:03  
Yeah, well, the recording has begun.  
Recording has begun.

![](file:////Users/kevin/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image006.jpg)**Tronkowski, Kevin**   0:08  
Alright, let's look at those pages.

![](file:////Users/kevin/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image004.jpg)**Bennett, Ryan**   0:08  
So.

![](file:////Users/kevin/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image006.jpg)**Tronkowski, Kevin**   0:10  
Just.  
Oh, so wait, before we do that, maybe someone, maybe Ryan, you can bring them up. All right. So we'll on this question of the new logo and it was quite the topic today. So are you?
```

### Key Characteristics

**Downloaded format indicators:**
- Combined speaker+timestamp: `**Last, First**   timestamp`
- Embedded image URLs before each speaker line
- Meeting header with title, date, duration
- Multi-line content following speaker line
- No separator lines (`____`)
- Line breaks preserved with double spaces

### Cleaned Transcript (After Processing)

```markdown
## Transcript

**[[Bennett, Ryan|Ryan Bennett]]** 0:03

Yeah, well, the recording has begun.  
Recording has begun.

**[[Tronkowski, Kevin|Kevin Tronkowski]]** 0:08

Alright, let's look at those pages.

**[[Bennett, Ryan|Ryan Bennett]]** 0:08

So.

**[[Tronkowski, Kevin|Kevin Tronkowski]]** 0:10

Just.  
Oh, so wait, before we do that, maybe someone, maybe Ryan, you can bring them up. All right. So we'll on this question of the new logo and it was quite the topic today. So are you?
```

### Processing Command

```bash
# Use the downloaded format script
python ~/.copilot/skills/obsidian-meeting/scripts/clean_transcript_downloaded.py \
  "~/Documents/Obsidian/HPE/Meetings/2026-01-13 - Green and Magenta Design Discussion.md"

# Output:
# ✓ Cleaned transcript successfully
#   Processed 79 entries
#   First: Ryan Bennett at 1:05
#   Last: Ryan Bennett at 1:15
```

### Format Comparison

| Aspect | Direct Paste Format | Downloaded Format |
|--------|-------------------|-------------------|
| **Speaker line** | `Last, First` (separate line) | `**Last, First**   timestamp` |
| **Timestamp** | `0 minutes 3 seconds0:03` | `0:03` |
| **Images** | URL on separate line | URL embedded before speaker |
| **Header** | None | Meeting title, date, duration |
| **Separators** | `____` lines present | No separators |
| **Script** | `clean_transcript.py` | `clean_transcript_downloaded.py` |

### Detection Logic

When processing a meeting, detect format by checking for:

```python
# Downloaded format: **Name**   timestamp pattern
if re.search(r'\*\*[A-Za-z]+, [A-Za-z]+\*\*\s+\d{1,2}:\d{2}', transcript):
    use_downloaded_script()
    
# Direct paste format: Name on own line
elif re.search(r'^[A-Za-z]+, [A-Za-z]+$', transcript, re.MULTILINE):
    use_direct_paste_script()
```

**Best practice**: Try downloaded format script first as it's more common in recent usage.
