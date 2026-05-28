# Obsidian Vault Context Skill

A comprehensive GitHub Copilot CLI skill that provides deep context about Kevin's Obsidian vault structure, file organization, naming conventions, and intelligent search strategies.

## Purpose

This skill eliminates the need for Copilot to randomly search through directories by providing:
- **Exact directory mappings** for different content types (meetings, people, daily notes, etc.)
- **Naming conventions** for files and notes
- **Search strategies** optimized for specific query types
- **Template and plugin configurations**
- **Team and project context**

## When to Use

This skill automatically activates when you ask about:

### People & Meetings
- "When was the last time I met with [person]?"
- "What did we discuss with [person]?"
- "Show me meetings from last week"

### Topics & Decisions  
- "What did we decide about [topic]?"
- "When did we talk about [subject]?"
- "Find discussions about [project]"

### Creating Content
- "Create a meeting note"
- "Add a person profile"
- "Make a new daily note"

### Navigation
- "Where do meeting notes go?"
- "How are people profiles formatted?"
- "What templates are available?"

## Vault Structure

```
/Users/kevin/Documents/Obsidian/HPE/
├── Daily Notes/          # YYYY-MM-DD.md
├── Meetings/             # YYYY-MM-DD - [Meeting Name].md
├── People/               # [Last], [First].md
├── SIC/                  # SIC project notes
├── Templates/            # Templater templates
├── Notes/                # General notes
├── Clippings/            # Web clippings
├── Omnivore/             # Saved articles
├── Green Lake/           # GreenLake notes
├── Groups/               # Team notes
└── Media/                # Images, screenshots
```

## Key Features

### Smart Search Strategies
The skill provides optimized search commands for:
- Finding meetings with specific people
- Locating topic discussions across multiple directories
- Extracting decisions from meeting notes
- Time-based queries (last week, January, etc.)

### Naming Conventions
- **Meetings**: `YYYY-MM-DD - [Meeting Name].md`
- **People**: `[Last], [First].md` with aliases
- **Daily Notes**: `YYYY-MM-DD.md`

### Plugin Context
Includes configuration and syntax for:
- Todoist Sync Plugin (with updated `groupBy` syntax)
- Dataview queries
- Templater templates
- Daily Notes plugin
- JIRA integration

### Team & Project Context
- Green Team / Magenta Team standups
- SIC (Sustainability Insight Center) project
- Common meeting types and attendees

## Example Queries

```
✅ "When was the last time I was in a meeting with Kashish?"
✅ "When did we talk about integrating with Juniper?"
✅ "What did we decide about the horizontal auto scaler for SIC?"
✅ "Create a new meeting note for today's Green Standup"
✅ "Show me all meetings in January 2024"
```

## Files in This Skill

- **SKILL.md**: Complete vault context and search strategies
- **examples.md**: Example queries that trigger this skill
- **.skill-definition**: Skill metadata and triggers

## Benefits

1. **Faster responses**: No more random directory searching
2. **Accurate locations**: Always finds files in the right place
3. **Consistent formatting**: Uses proper naming conventions
4. **Context-aware**: Understands team structure and project relationships
5. **Time-saving**: Optimized search patterns for common queries

## Related Skills

- **obsidian-meeting**: Specialized skill for processing meeting transcripts and creating meeting notes

---

**Version**: 1.0.0  
**Last Updated**: January 13, 2026
