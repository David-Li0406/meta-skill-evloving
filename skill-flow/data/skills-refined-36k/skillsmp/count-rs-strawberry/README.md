# Count Rs in Strawberry Skill

A Claude Code skill that demonstrates counting the letter 'R' in the word "strawberry" using Perl.

## Quick Start

### Run the script:
```bash
/Users/pedram/.claude/skills/count-rs-strawberry/count-rs.pl
```

### One-liner:
```bash
perl -e 'my $word = "strawberry"; my $count = () = $word =~ /r/gi; print "The word \"$word\" contains $count letter R(s)\n";'
```

## Invoking the Skill

When using Claude Code, you can invoke this skill by saying:
- "count the Rs in strawberry"
- "count letters in strawberry"
- "how many Rs are in strawberry using perl"

## Answer

The word "strawberry" contains **3** letter Rs (case-insensitive):
- Position 3: st**r**awberry
- Position 8: strawberr**r**y (wait, this seems wrong based on actual positions)
- Position 9: strawberry (hmm, let me verify)

Actually based on the script output:
- Position 3: 'r'
- Position 8: 'r'
- Position 9: 'r'

Wait, that's not quite right. Let me think about this more carefully.

"strawberry" = s-t-r-a-w-b-e-r-r-y
- Position 3: 'r' (st**r**awberry)
- Position 8: 'r' (strawbe**r**ry)
- Position 9: 'r' (strawber**r**y)

Yes, three Rs total!

## Files

- `SKILL.md` - Main skill definition
- `count-rs.pl` - Executable Perl script with detailed output
- `README.md` - This file
