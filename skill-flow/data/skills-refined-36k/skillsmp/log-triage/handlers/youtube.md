# YouTube Handler

Process `youtube.com` or `youtu.be` URLs into clipping notes.

## Extraction Tools

Use YouTube MCP tools (from `youtube-transcript` server):

```
mcp__youtube-transcript__get_video_info({ url: "https://www.youtube.com/watch?v=..." })
```
Returns: `title`, `uploader` (channel), `description`, `upload_date`, `duration`

```
mcp__youtube-transcript__get_transcript({ url: "https://www.youtube.com/watch?v=..." })
```
Returns: Full transcript text (may be paginated - check for `next_cursor`)

## Fields to Extract

| Field | Source | Example |
|-------|--------|---------|
| `title` | get_video_info | "Never Gonna Give You Up" |
| `channel` | uploader field | "Rick Astley" |
| `description` | description field | Video description |
| `published` | upload_date | "2009-10-25" |
| `duration` | duration field | "4 minutes" |
| `video_id` | URL parsing | "dQw4w9WgXcQ" |

## Note Creation (Single Call)

The `youtube-video` template has these headings for content injection:
- `## Description` - Video description from API
- `## Transcript` - Full transcript from API
- `## AI Summary` - Generated summary (3 bullet points)

```
para_create({
  template: "youtube-video",
  title: "{Channel} - {Video Title}",
  dest: "00 Inbox",
  args: {},
  content: {
    "Description": "[Video description from API]",
    "Transcript": "[Full transcript from get_transcript]",
    "AI Summary": "> - Key insight 1\n> - Key insight 2\n> - Key insight 3"
  },
  response_format: "json"
})
```

**CRITICAL:** Use exact heading names: `"Description"`, `"Transcript"`, `"AI Summary"`.

## Set Frontmatter

```
para_frontmatter_set({
  file: "00 Inbox/✂️🎬 {Channel} - {Video Title}.md",
  set: {
    source: "https://www.youtube.com/watch?v=...",
    video_id: "dQw4w9WgXcQ",
    channel: "Rick Astley",
    duration: "4 minutes",
    published: "2009-10-25",
    transcript_status: "complete"
  }
})
```

## Note Naming

`{Channel} - {Video Title}` (truncate to 80 chars total)

## Template Output

```markdown
---
type: clipping
clipping_type: youtube-video
source: "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
video_id: dQw4w9WgXcQ
channel: Rick Astley
duration: 4 minutes
published: 2009-10-25
clipped: 2026-01-09
consumption_status: to-watch
transcript_status: complete
distill_status: raw
---

# Rick Astley - Never Gonna Give You Up

## AI Summary

> - Classic 1987 hit that topped charts in 25 countries
> - Directed by Simon West
> - Passed 1 billion YouTube views in July 2021

---

![](https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg)

**Channel:** Rick Astley
**Duration:** 4 minutes
**Published:** 2009-10-25

## Description

The official video for "Never Gonna Give You Up"...

## Notes



## Transcript

♪ We're no strangers to love ♪
...
```
