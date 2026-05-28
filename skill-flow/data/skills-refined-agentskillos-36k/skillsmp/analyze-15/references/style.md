# Style Analysis Reference

## Analysis Criteria

Focus on normalization - there should be ONE way of doing things. Majority pattern wins - align outliers to dominant pattern. Respect existing patterns and work with the codebase, not against it.

### Naming

- Inconsistent naming conventions across files
- Mixed camelCase/snake_case within same context
- Inconsistent abbreviations (btn vs button, msg vs message)
- Non-descriptive names that obscure intent

### Patterns

- Different ways of handling the same thing
- Inconsistent error handling patterns
- Mixed async patterns (callbacks vs promises vs async/await)
- Inconsistent component patterns in UI code
- Different state management approaches

### Structure

- Inconsistent file organization
- Mixed import styles (default vs named, relative vs absolute)
- Inconsistent export patterns (named vs default vs barrel)
- Module organization inconsistencies

### Formatting

- Issues not caught by automated formatters
- Inconsistent whitespace in logic blocks
- Comment style inconsistencies
- Inconsistent brace/bracket placement

## Pattern Detection Tables

### Naming Conventions

| Pattern    | Variations to Detect                                |
| ---------- | --------------------------------------------------- |
| Functions  | `getUserData` vs `get_user_data` vs `GetUserData`   |
| Variables  | `isLoading` vs `loading` vs `is_loading`            |
| Constants  | `MAX_RETRIES` vs `maxRetries` vs `MaxRetries`       |
| Components | `UserCard` vs `userCard` vs `User_Card`             |
| Files      | `UserCard.tsx` vs `user-card.tsx` vs `userCard.tsx` |

### Code Patterns

| Area           | Variations to Detect                      |
| -------------- | ----------------------------------------- |
| Error handling | try/catch vs .catch() vs error boundaries |
| Async          | async/await vs .then() vs callbacks       |
| State updates  | setState vs reducer vs signals            |
| Props          | destructuring vs props.x                  |
| Exports        | named vs default vs barrel files          |

## Severity Guidelines

- **Critical**: Fundamental inconsistencies that significantly harm readability
- **High**: Major deviations from established patterns in key areas
- **Medium**: Noticeable inconsistencies that create friction
- **Low**: Minor style variations, cosmetic issues

## Notes

Include in the `notes` field when relevant:

- The established project standard for this pattern
- Count of files following majority pattern vs outliers
- Whether this is a naming, pattern, structure, or formatting issue
- Other files with the same inconsistency
