<overview>
Clean code principles based on Robert Martin's Clean Code and industry research. SOLID principles, naming conventions, and code smell detection.
</overview>

<solid_principles>
| Principle | Rule | Violation Sign |
|-----------|------|----------------|
| **S**ingle Responsibility | One reason to change | Class/function does multiple things |
| **O**pen/Closed | Open for extension, closed for modification | Adding features requires changing existing code |
| **L**iskov Substitution | Subtypes must be substitutable | Subclass breaks when used as parent |
| **I**nterface Segregation | No forced dependencies | Implementing unused interface methods |
| **D**ependency Inversion | Depend on abstractions | Direct instantiation of dependencies |
</solid_principles>

<function_guidelines>
<size_and_scope>
Function size targets:

- Maximum 50 lines (ideally <20)
- Do ONE thing well
- Single level of abstraction
- Fit on one screen without scrolling
  </size_and_scope>

<parameters>
Parameter limits:

- Maximum 3 parameters
- Avoid flag arguments (split into separate methods)
- Use objects for related parameters
  </parameters>

<naming>
Function naming patterns:

- Verbs for functions: `getUserById()`, `calculateTotal()`
- Reveals intent without reading body
- No abbreviations: `getTransaction()` not `getTx()`
  </naming>
  </function_guidelines>

<naming_conventions>
General naming rules:

✓ Descriptive, unambiguous names
✓ Pronounceable and searchable
✓ Class names: nouns (User, PaymentProcessor)
✓ Method names: verbs (validate, calculate, fetch)
✗ Single letter variables (except loop counters)
✗ Hungarian notation (strName, intCount)
✗ Abbreviations (usr, txn, cfg)
</naming_conventions>

<code_smells>
<critical_smells>
Flag these in review:

| Smell                   | Detection                             | Fix                        |
| ----------------------- | ------------------------------------- | -------------------------- |
| **Duplicated Code**     | Same logic in 2+ places               | Extract to shared function |
| **Large Class/Method**  | >50 lines, multiple responsibilities  | Split by responsibility    |
| **Long Parameter List** | >3 parameters                         | Use parameter object       |
| **Feature Envy**        | Method uses another class's data more | Move method to that class  |
| **God Object**          | One class controls everything         | Split into focused classes |

</critical_smells>

<medium_smells>
Suggest these fixes:

| Smell               | Detection                         | Fix                          |
| ------------------- | --------------------------------- | ---------------------------- |
| **Deep Nesting**    | >3 levels of indentation          | Guard clauses, early returns |
| **Magic Numbers**   | Unexplained literals              | Named constants              |
| **Dead Code**       | Commented-out or unreachable code | Delete it                    |
| **Shotgun Surgery** | Small change touches many files   | Consolidate related code     |

</medium_smells>
</code_smells>

<complexity_reduction>
<example_before>
Complex nested conditions:

```javascript
function process(user) {
  if (user) {
    if (user.isActive) {
      if (user.hasPermission) {
        // actual logic here
      }
    }
  }
}
```

</example_before>

<example_after>
Simplified with guard clauses:

```javascript
function process(user) {
  if (!user) return;
  if (!user.isActive) return;
  if (!user.hasPermission) return;

  // actual logic here
}
```

</example_after>
</complexity_reduction>

<comments_best_practices>
<good_comments>
Valuable comments explain:

- Explain WHY (intent), not WHAT (code does that)
- Warn of consequences
- TODO with ticket number
  </good_comments>

<bad_comments>
Avoid these comment types:

- Redundant (restates the code)
- Commented-out code (delete it)
- Closing brace comments (`} // end if`)
- Journal comments (use git history)
  </bad_comments>
  </comments_best_practices>

<boy_scout_rule>

> Leave code cleaner than you found it.

**Important**: In PRs, only clean code already being changed. Don't expand scope.
</boy_scout_rule>

<sources>
- Clean Code by Robert C. Martin
- [Google Engineering Practices](https://google.github.io/eng-practices/)
- [Microsoft Code Review Guide](https://microsoft.github.io/code-with-engineering-playbook/)
</sources>
