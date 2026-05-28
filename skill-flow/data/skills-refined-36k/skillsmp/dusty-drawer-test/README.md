# The Dusty Drawer Test

A framework for evaluating whether a research project will have real impact, or end up forgotten in a drawer.

## What it is

A structured way to ask: "Will anyone do something differently because of this work?"

The framework gives you:
- 7 foundational concepts from evaluation science, psychology, and systems thinking
- 7 evaluation questions that make implicit assumptions explicit
- Classification tools for assessing risk and realistic impact ceiling

## Installation

Copy `SKILL.md` to your Claude skills directory:

```
~/.claude/skills/dusty-drawer-test/SKILL.md
```

Or wherever your Claude installation looks for user skills.

## Usage

Ask Claude to evaluate a project:

> "Apply the dusty drawer test to this project proposal: [description]"

Or:

> "Review this project from an impact perspective: [description]"

Claude will return a structured assessment with:
- Scores on 7 dimensions (0-2 each, /14 total)
- Pull classification (Pulled / Revealed / Pushed)
- Impact ladder ceiling
- Specific strengths, weaknesses, and recommendations

## The core question

**Impact = someone did something they otherwise wouldn't have.**

If your work doesn't change anyone's decisions, behavior, or understanding (including your own), it has no impact regardless of quality.

## Foundations

The framework rests on 7 concepts.

**What impact is:**
1. Counterfactual thinking: impact means *additional* change
2. Pragmatism: ideas without consequences are empty
3. Systems leverage: higher impact, less control
4. Neglectedness: marginal contribution matters
5. Theory of Change: causal pathways with testable assumptions

**The human side:**
6. Task separation: control what's yours, release the rest
7. Feedback loops: sustain motivation through intermediate signals

See [docs/whitepaper.md](docs/whitepaper.md) for theoretical foundations and references.

## Evaluation questions

| # | Question | What it tests |
|---|----------|---------------|
| 1 | **Who?** | Who will carry this up the ladder? Can you name them? |
| 2 | **What change?** | What will they do differently, and how direct is the path? |
| 3 | **Causal path?** | What assumptions connect your output to impact? |
| 4 | **Fit?** | Why you/your team vs. anyone else? |
| 5 | **Values?** | Does this leave things better? |
| 6 | **Feedback?** | How long until you know if it worked? |
| 7 | **Control?** | What's yours to control vs. others'? |

## Scoring

- **Below 7/14:** Likely to struggle. Reframe or pass.
- **7-10/14:** Proceed with eyes open. Address weaknesses.
- **11-14/14:** Strong candidate. Protect this work.

## License

Apache 2.0. See [LICENSE](LICENSE).

## Acknowledgments

Built on work by: GiveWell (counterfactual analysis), William James and John Dewey (pragmatism), Donella Meadows (systems leverage), 80,000 Hours (ITN framework), Carol Weiss (Theory of Change), Alfred Adler (task separation), Albert Bandura (self-efficacy).
