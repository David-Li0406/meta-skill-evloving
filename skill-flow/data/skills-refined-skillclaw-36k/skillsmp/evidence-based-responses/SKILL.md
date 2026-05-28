---
name: evidence-based-responses
description: Guide for writing and responding to code review comments with evidence-based claims. Use when writing PR review comments, responding to reviewer feedback, or engaging in technical discussions where claims should be backed by documentation, code references, or test results. Covers research and validation before making claims, linking to evidence, and professional communication.
---

# Evidence-Based Responses

Never make a technical claim without evidence to back it up. When someone asks "does X work this way?" or "shouldn't this be Y?", the answer should include a link to documentation, a code reference, or test results that demonstrate the claim is true.

## Responding to Review Comments

When a reviewer raises a concern, follow this workflow: first understand what they're actually asking (not what you assume they're asking), then research to verify the facts, gather concrete evidence, and finally draft a response that addresses their concern directly.

Start by acknowledging valid points. Phrases like "Good catch" or "You're right that..." show you've genuinely considered their feedback. If they've identified a real issue, thank them and explain how you're addressing it. If their concern is based on a misunderstanding, clarify with evidence rather than dismissing the concern.

Address the reviewer's actual question. If they ask "should this constant be dynamic?", don't just say "no" or "yes". Explain why the current approach works (or doesn't), cite the relevant documentation or code behavior, and link to any changes you've made in response.

See [references/response-examples.md](references/response-examples.md) for concrete examples of well-structured responses.

## Writing Review Comments

When writing a review comment, lead with the concern rather than the solution. Explain what you've observed and why it might be problematic, then provide evidence for your concern. If you're suggesting a change, explain the reasoning and offer alternatives when possible.

Avoid drive-by comments that just say "this is wrong" without explanation. If you're not sure something is actually a problem, frame it as a question: "I noticed X, which might cause Y. Was this intentional?" This invites discussion rather than putting the author on the defensive.

When proposing code changes, use GitHub's suggestion blocks so the author can apply your suggestion directly. This makes it easy for them to accept your feedback and reduces friction.

## Validation Before Claiming

Before asserting that something behaves a certain way, verify it. The type of verification depends on the claim.

For language or framework behavior, cite official documentation. If you claim "Ruby constants are evaluated once at assignment time", link to the Ruby docs or Rails guides that confirm this. When documentation is ambiguous, write a small test to confirm the behavior and mention that you tested it.

For claims about how code in the repository works, link to the specific file and line numbers. Use permalink URLs with commit SHAs rather than branch names so the links remain valid even after the code changes. If you've made changes that address the concern, link to the commit.

For claims about system architecture (like "this data persists indefinitely"), trace the data flow through the code to find the backing store, configuration, or service. Link to the relevant implementation files and explain what you found.

See [references/validation-techniques.md](references/validation-techniques.md) for detailed research methods.

## GitHub Link Formats

Use commit SHAs in links so they remain valid over time. The format `https://github.com/org/repo/blob/<sha>/path/to/file.rb#L123` creates a permalink to a specific line. For line ranges, use `#L10-L20`.

When referencing commits, you can use the short SHA inline (like "fixed in abc123") or provide the full URL for easier navigation. GitHub automatically links commit SHAs in comments.

For suggesting code changes, use suggestion blocks:

````
```suggestion
the corrected code here
```
````

This lets the author apply your suggestion with one click.

## Style

Write in prose and paragraphs rather than bullet lists. A well-constructed paragraph flows better and communicates more naturally than a wall of bullet points.

Avoid emdashes. Use commas, parentheses, or separate sentences instead.

Keep responses concise but complete. Say what needs to be said, provide the necessary evidence, and stop. Don't pad responses with unnecessary qualifications or repetition.

Be friendly and direct. You can be professional without being cold, and direct without being harsh. Assume good intent from reviewers and authors alike.
