<overview>
Code review feedback patterns based on research from Google, Microsoft, and academic studies on effective code review communication.
</overview>

<what_why_how_pattern>
Every valuable comment includes three components:

1. **What**: The specific issue
2. **Why**: Why it matters
3. **How**: Concrete fix or direction

<good_example>

```
[BLOCKING] SQL injection vulnerability at line 34.
The query uses string concatenation with user input, allowing attackers to modify the query.
Fix: Use parameterized query: db.query('SELECT * FROM users WHERE id = ?', [userId])
```

</good_example>

<bad_example>

```
This query looks unsafe.
```

</bad_example>
</what_why_how_pattern>

<priority_labels>
Use consistent labels so authors know severity:

| Label          | Meaning                                           | Merge?  |
| -------------- | ------------------------------------------------- | ------- |
| `[BLOCKING]`   | Must fix - security, bugs, missing requirements   | No      |
| `[CRITICAL]`   | Strongly recommended - architecture, major issues | Discuss |
| `[SUGGESTION]` | Would improve code - not required                 | Yes     |
| `[NIT]`        | Minor preference - skip if busy                   | Yes     |
| `[QUESTION]`   | Need clarification - not blocking                 | Yes     |

</priority_labels>

<feedback_value>
<high_value>
High-value feedback (36-43% implementation rate):

- Security vulnerabilities with exploit scenario
- Logic errors with failing test case
- Missing error handling with consequences
- Performance issues with measurements
  </high_value>

<wasteful>
Wasteful feedback (damages team dynamics):

- Style preferences covered by linters
- Renaming suggestions without clear benefit
- "I would do it differently" without why
- Comments on code outside the diff
  </wasteful>
  </feedback_value>

<communication_patterns>
<collaborative_framing>
Use collaborative, question-based framing:

```
✓ "Have you considered using a Map here for O(1) lookup?"
✓ "This could throw if user is null - should we add a check?"
✓ "I'm not sure I understand this logic - could you explain?"

✗ "You need to fix this."
✗ "This is wrong."
✗ "Obviously this should be..."
```

</collaborative_framing>

<avoid_belittling>
Remove belittling words: "just", "simply", "obviously", "easy", "only"

```
✗ "Just add a null check"
✗ "This is obviously wrong"
✓ "Add a null check for user.profile"
```

</avoid_belittling>
</communication_patterns>

<merge_decisions>
<block_merge>
Block merge for:

- Security vulnerabilities (any severity)
- Logic bugs that affect functionality
- Missing required tests
- Breaking API changes without migration
  </block_merge>

<approve_with_comments>
Approve with comments for:

- Suggestions for future improvement
- Minor refactoring opportunities
- Documentation improvements
- Style preferences (should be in linter)
  </approve_with_comments>

<approve_clean>
Approve cleanly when:

- Code meets requirements
- Tests pass
- No security issues
- Follows project conventions
  </approve_clean>
  </merge_decisions>

<avoiding_nitpick_culture>
**Research finding**: Nitpicking damages team relationships more than it improves code quality. Developers become defensive and less receptive to legitimate feedback.

<solution>
1. Automate style enforcement (linters, formatters)
2. Block CI on lint failures, not PR comments
3. Reserve human review for logic and design
4. Mark true nitpicks with `[NIT]` prefix
5. Limit to 3-5 critical items per review
</solution>
</avoiding_nitpick_culture>

<review_efficiency>
<google_data>
Google's review data shows:

- 90% of reviews: <10 files changed
- Average turnaround: 4 hours
- 75% need only one reviewer
  </google_data>

<best_practices>
Efficiency best practices:

- Small PRs get better feedback
- Review within 4 hours if possible
- Focus on changed code only
- One pass, thorough, then done
  </best_practices>
  </review_efficiency>

<sources>
- [Google Code Review Guide](https://google.github.io/eng-practices/review/)
- [Microsoft Reviewer Guidance](https://microsoft.github.io/code-with-engineering-playbook/code-reviews/)
- [Conventional Comments](https://conventionalcomments.org/)
</sources>
