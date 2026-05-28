# Teams Clipboard Format

When you copy chat content from Teams, it uses a specific text format. Parse this natively.

## Message Structure

Each message block follows this pattern:

```
AuthorName
DD/MM/YYYY H:MM am/pm
Message content here
Can span multiple lines
```

**Example:**
```
Jay Pancholi
15/01/2025 2:34 pm
Hey Nathan, just checking in on the project status.
Let me know when you have a moment.
```

## Replies (Reference Blocks)

Replies to messages appear as:

```
Begin Reference, preview of quoted message by OriginalAuthor
Quoted content snippet...
End Reference
Reply content here
```

**Example:**
```
Nathan Vale
15/01/2025 2:45 pm
Begin Reference, preview of Hey Nathan, just checking in on the project status. by Jay Pancholi
End Reference
All good! I'll have the update ready by EOD.
```

## Reactions

Reactions appear after message content:

```
emoji
N emoji-name reactions.
```

**Example:**
```
👍
2 like reactions.
❤️
1 heart reactions.
```

## Attachments

Various attachment indicators:

| Type | Pattern |
|------|---------|
| GIF | `(GIF Image)` |
| Image | `(Image)` or filename like `Screenshot 2025-01-15.png` |
| File | `has an attachment: filename.pdf` |
| URL Preview | `Url Preview for https://...` |
| Loop Component | `Loop Component` |

## Mentions

- **Direct mention:** Name appears inline in message text
- **@everyone:** Appears as `Everyone` in message text

## Edited Messages

Edited messages include:

```
Message content
Edited.
```
