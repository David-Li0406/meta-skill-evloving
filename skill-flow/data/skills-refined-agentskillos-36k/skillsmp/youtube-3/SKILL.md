---
name: youtube
description: Search YouTube videos via Invidious. Auto-triggers when user asks to find, search for, or look up videos.
---

# YouTube Video Search

Search YouTube videos using the Invidious API at `https://yt.tarka.dev`.

## When to Use

Auto-trigger this skill when the user:

- Asks to "find a video about..."
- Asks to "search YouTube for..."
- Asks to "look up videos on..."
- Wants video recommendations on a topic
- Asks "are there any videos about..."

## How to Search

Use WebFetch to query the Invidious API:

```
https://yt.tarka.dev/api/v1/search?q=<query>&type=video
```

## Formatting Results

Format each video as a markdown list item:

- [**{title}**](https://yt.tarka.dev/watch?v={videoId}) by {author} - {viewCountText} - {publishedText} - Duration: {duration}

### Duration Formatting

Convert `lengthSeconds` to human-readable format:

- Under 1 hour: `MM:SS` (e.g., `12:34`)
- 1 hour or more: `H:MM:SS` (e.g., `1:23:45`)



## Example

When user asks "find me a video about Clojure macros":

- [**Clojure Tutorial**](https://yt.tarka.dev/watch?v=ciGyHkDuPAE) by Derek Banas - 175K views - 8 years ago - Duration: 1:11:23

Show 3-5 results by default.

## Notes

- Always use `https://yt.tarka.dev` (user's Invidious instance)
- If no results, suggest alternative search terms
