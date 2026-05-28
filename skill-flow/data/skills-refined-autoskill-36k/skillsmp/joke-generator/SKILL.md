---
name: joke-generator
description: Generate jokes from various categories (programming, dad, science, general) to bring some humor. Use when the user asks for a joke or wants to lighten the mood.
argument-hint: [category]
---

When this skill is invoked with $ARGUMENTS:

1. Determine the joke category:
   - If specified, use that category
   - If not specified or "random", pick a random category

2. Select or generate a joke from these collections:

   **Programming jokes:**
   - Why do programmers prefer dark mode? Because light attracts bugs!
   - How many programmers does it take to change a light bulb? None, that's a hardware problem!
   - Why did the programmer quit? Because they didn't get arrays!
   - A SQL query walks into a bar, walks up to two tables and asks: "Can I join you?"

   **Dad jokes:**
   - I'm afraid for the calendar. Its days are numbered!
   - Why don't scientists trust atoms? Because they make up everything!
   - What do you call a fake noodle? An impasta!
   - I used to hate facial hair, but then it grew on me!

   **Science jokes:**
   - Two atoms are walking down the street. One says, "I think I lost an electron!" The other asks, "Are you positive?"
   - What did the thermometer say to the graduated cylinder? "You may have graduated, but I have more degrees!"
   - Why can't you trust an atom? They make up everything!

   **General jokes:**
   - What do you call a bear with no teeth? A gummy bear!
   - Why did the scarecrow win an award? He was outstanding in his field!
   - What's orange and sounds like a parrot? A carrot!

3. Present the joke with an appropriate emoji (😄, 🤣, 😂, or category-specific like 💻 for programming)

4. If the user requests a category that doesn't exist, list available categories

5. Keep it light and fun!

## Categories

- **programming** - Developer and coding humor
- **dad** - Classic groan-worthy dad jokes
- **science** - Jokes about science and scientists
- **general** - General clean humor
- **random** - Pick any category randomly

## Examples

```
User: /joke-generator programming
Result: Why do programmers prefer dark mode? Because light attracts bugs! 🐛
```

```
User: /joke-generator dad
Result: I'm afraid for the calendar. Its days are numbered! 😄
```
