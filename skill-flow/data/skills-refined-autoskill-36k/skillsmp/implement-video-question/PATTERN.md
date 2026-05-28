# Video Question Pattern

## Overview

Questions where students watch a video as the primary instructional content and provide written responses.

## Visual Structure

```
┌──────────────────────────────────────────┐
│ Video Reflection                         │
│ Watch the video and answer the question. │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│ ▶ [Video Player]                         │
│                                          │
│ Watch this explanation of proportional   │
│ relationships                            │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│ What is the main concept explained?      │
│                                          │
│ ┌──────────────────────────────────────┐ │
│ │ Type your answer here...             │ │
│ │                                      │ │
│ │                                      │ │
│ │                                      │ │
│ └──────────────────────────────────────┘ │
└──────────────────────────────────────────┘
```

## When to Use

- Video is the primary instructional content
- Students watch and reflect
- Written analysis of visual demonstrations
- Video-based lessons requiring comprehension checks

## State Shape

### Single Response
```javascript
{
  explanation: ""
}
```

### Multiple Responses
```javascript
{
  response1: "",
  response2: "",
  response3: ""
}
```

## Component Flow

1. **Intro Card** (optional) - Sets context and expectations
2. **Video Player** - Primary instructional content
3. **Response Card(s)** - Written reflection/answers

## Interaction Pattern

1. Student watches video (can pause, replay)
2. Student types response in textarea
3. State auto-saves on every input
4. Response preserved across sessions

## Comparison with Text Response

| Video Question | Text Response Question |
|----------------|------------------------|
| Video is required, primary content | No video, or video is optional |
| Watch → Respond | Read → Respond |
| Uses video-response.js snippet | Uses cards directly |
| Video provides the instruction | Text/images provide context |
