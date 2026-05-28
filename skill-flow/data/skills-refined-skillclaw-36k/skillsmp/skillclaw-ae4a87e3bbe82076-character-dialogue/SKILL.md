---
name: character-dialogue
description: Use this skill when you need to format character names and dialogue in Fountain format, including handling extensions, dual dialogue, and parentheticals.
---

# Character & Dialogue Skill

## Invocation Triggers
Apply this skill when:
- Introducing characters
- Writing dialogue blocks
- Formatting character names
- Handling dual dialogue
- Using character extensions

## Character Name Format

### Basic Format
Character names must be:
- ALL UPPERCASE
- On their own line
- Preceded by a blank line
- Followed immediately by dialogue (no blank line)

```fountain

SARAH
Hello, John.
```

### Character Extensions
Extensions appear in parentheses after the name:

| Extension | Meaning | When to Use |
|-----------|---------|-------------|
| `(V.O.)` | Voice Over | Character narrating or not in scene |
| `(O.S.)` | Off Screen | Character in scene but not visible |
| `(O.C.)` | Off Camera | Same as O.S. (alternate) |
| `(CONT'D)` | Continued | Same speaker after action interruption |
| `(PRE-LAP)` | Pre-lap | Audio starts before scene |
| `(INTO PHONE)` | Delivery | Speaking into phone |
| `(INTO RADIO)` | Delivery | Speaking into radio |
| `(SUBTITLE)` | Translation | Foreign dialogue translated |

```fountain
SARAH (V.O.)
I never should have trusted him.

JOHN (O.S.)
Sarah? Are you home?

SARAH
In here!

She turns toward the door.

SARAH (CONT'D)
I wasn't expecting you.
```

### Forcing Mixed-Case Names
Use `@` prefix for names that aren't all caps:
```fountain
@McCLANE
Yippee ki-yay.

@DeVITO
Don't start with me.
```

## Dialogue Format

### Basic Dialogue
```fountain
SARAH
This is a line of dialogue. It can
span multiple lines naturally.
```

### Dialogue with Parenthetical
```fountain
SARAH
(hesitant)
I don't think that's a good idea.

JOHN
(laughing)
You always say that.
(serious now)
But this time I agree.
```

### Parenthetical Guidelines
- Use sparingly
- Brief direction only
- Lower case
- On own line within dialogue block
- Don't overuse - trust actors

**Good parentheticals:**
```fountain
(whispering)
(to John)
(beat)
(re: the gun)
(into phone)
```

**Bad parentheticals (avoid):**
```fountain
(angrily, as if she can't believe what she's hearing)
(walking across the room and picking up the vase)
```