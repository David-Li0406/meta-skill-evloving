---
name: mockumentary-screenplay
description: Write mockumentary screenplays in Fountain format with proper documentary conventions, talking head formatting, and comedic dialogue. Use when user needs to write screenplay pages, format talking heads, write verite scenes, craft dialogue, or convert outline to script. Triggers on screenplay writing, Fountain formatting, dialogue writing, scene writing, or drafting for mockumentary projects.
---

# Mockumentary Screenplay Writing

Write screenplays in Fountain format with mockumentary-specific conventions.

## Fountain Format Basics

Fountain is plain text that converts to industry-standard screenplay format.

### Core Elements

```fountain
INT. LOCATION - DAY

Action lines describe what we see.

CHARACTER NAME
Dialogue goes here.

CHARACTER NAME (V.O.)
Voiceover dialogue.

CHARACTER NAME (O.S.)
Offscreen dialogue.
```

### Scene Headings

```fountain
INT. OFFICE - TALKING HEAD - DAY

INT. DOG SHOW - ARENA FLOOR - CONTINUOUS

EXT. PARKING LOT - LATER
```

### Parentheticals (Use Sparingly)

```fountain
CHARACTER
(beat)
The line after a pause.

CHARACTER
(to other character)
Specific direction.
```

## Mockumentary-Specific Formatting

### Talking Head Interviews

```fountain
INT. CONFERENCE ROOM - TALKING HEAD - DAY

MICHAEL sits before a neutral background, speaking to someone off-camera.

MICHAEL
I'm not superstitious. But I am a little stitious.

He looks off-camera as if for validation.
```

**Key elements**:
- Scene heading includes "TALKING HEAD"
- Brief action line establishing setting
- Character speaks to off-camera interviewer
- Include looks to camera, pauses, reactions

### Documentary Crew Interaction

```fountain
INT. OFFICE - DAY

MICHAEL notices the camera.

MICHAEL
(to camera)
Watch this. This is going to be great.

He approaches DWIGHT's desk. The camera follows.
```

### Multiple Camera Angles (Documentary Style)

```fountain
INT. ARENA - DAY

WIDE: The competitors line up with their dogs.

The camera finds HARLAN in the crowd, adjusting his dog's collar obsessively.

HARLAN
(sotto, to dog)
This is our moment, Mr. Biscuits.
```

### Cutaway/B-Roll

```fountain
INT. FACTORY FLOOR - B-ROLL - DAY

Workers operate machinery. Assembly line in motion.

NARRATOR (V.O.)
Prestige Pickle has been family-owned for three generations.
```

### Interview with Cutaways

```fountain
INT. OFFICE - TALKING HEAD - DAY

SUSAN
We have an excellent safety record.

CUT TO:

INT. FACTORY FLOOR - DAY (ARCHIVAL)

A forklift tips over. Workers scatter.

BACK TO:

INT. OFFICE - TALKING HEAD - DAY

SUSAN
Excellent.
```

## Writing Mockumentary Dialogue

### Talking Head Voice Principles

**Oversharing**: Characters tell camera things they shouldn't.
```fountain
MICHAEL
Jan and I have a very mature relationship. We never fight. 
(beat)
Except about money. And her ex-husband. And Todd Packer.
```

**False confidence**: Characters state the wrong thing with certainty.
```fountain
NIGEL
This one goes to eleven. It's one louder, isn't it?
```

**Unreliable narration**: What they say contradicts what we see.
```fountain
NARRATOR (V.O.)
The team worked together seamlessly.

WIDE: The team argues loudly.
```

### Verite Scene Dialogue

**Naturalistic overlap**:
```fountain
TEAM MEMBER 1
What we need to do is—

TEAM MEMBER 2
—No, but that's exactly what I was—

TEAM MEMBER 1
—Let me finish—

TEAM MEMBER 2
I'm agreeing with you!
```

**Camera awareness bleed**:
```fountain
JOHN
(noticing camera)
Oh, we're still—
(to team, lower)
They're still filming.
```

## Scene Construction

### The Mockumentary Beat Pattern

1. **Setup** (verite or interview establishes situation)
2. **Escalation** (situation develops, comic tension builds)
3. **Payoff** (comic climax, often ironic)
4. **Tag** (talking head reaction, often undercuts or confirms)

### Example Beat Pattern

```fountain
INT. MEETING ROOM - DAY

MANAGER addresses the team confidently.

MANAGER
This quarter, we're going to crush it.

CUT TO:

INT. OFFICE - TALKING HEAD - DAY

MANAGER
(less confident)
Define "crush."

CUT TO:

INT. MEETING ROOM - DAY

The sales chart shows a steep decline. MANAGER ignores it.

MANAGER (CONT'D)
Any questions? No? Great.

CUT TO:

INT. OFFICE - TALKING HEAD - DAY

EMPLOYEE
There were many questions.
```

## Output Format

Save screenplay to: `script/screenplay.fountain`

Fountain files are plain text and render to PDF via various tools (Highland, WriterSolo, Fountain.io).

## Page Count Guidelines

- Feature mockumentary: 80-100 pages
- TV pilot: 22-32 pages (half-hour), 45-60 pages (hour)
- Talking heads: Should not exceed 25% of page count
