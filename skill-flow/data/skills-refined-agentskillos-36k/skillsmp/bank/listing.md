# Listing Content

List and browse the content bank—view topics and explore stored content.

## Pre-check

Before listing, check if `content-bank/topics.md` exists. If not, inform the user the content bank is empty and offer to bank some content first.

## Capabilities

### List Topics

Display all available topics from `content-bank/topics.md`:

```
Your content bank topics:

**Writing:**
- productivity-systems (8 entries)
- writing-craft (5 entries)
- technical-communication (3 entries)

**Code:**
- error-handling (6 entries)
- async-patterns (4 entries)
- react-components (7 entries)
```

### Browse Topic

Show contents of a specific topic folder:

```
Contents of "error-handling":

**Ideas (2):**
- Fail-fast vs fail-safe tradeoffs
- Error categorization strategy

**Snippets (3):**
- Retry with exponential backoff (TypeScript)
- Error boundary HOC (React)
- Custom error classes (TypeScript)

**Outlines (1):**
- API error handling architecture
```

### Filter by Type

Show only writing or code content:

```
Code content in "async-patterns":

**Snippets:**
- Promise.all with error handling (TypeScript)
- Async queue implementation (TypeScript)
- Debounce utility (JavaScript)
```

## Usage

```
Show my content bank topics
List topics
What topics do I have?

Show what's in {topic}
Browse {topic}
What's in {topic}?

Show code topics
Show writing topics
List {language} snippets
```
