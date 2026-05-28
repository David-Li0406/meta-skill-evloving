---
name: norminette-checker
description: Check and fix C code according to 42 School's Norminette standards. Use when checking code style, before committing, or when user mentions norm/norminette.
---

# Norminette Checker

Automatically verify C code compliance with 42 School's Norminette standards.

## Key Norminette Rules

### File Structure
- **Header**: Standard 42 header required in all files
- **Header Guards**: `#ifndef`, `#define`, `#endif` in .h files
- **Max Line Length**: 80 characters (including newline)
- **Max Function Length**: 25 lines
- **Functions per File**: Maximum 5 functions

### Formatting Rules
- **Indentation**: Tabs only (no spaces)
- **Control Structure Braces**:
  ```c
  if (condition)
  {
      // code on new line
  }
  ```
- **Function Braces**:
  ```c
  int function(void)
  {
      // opening brace on new line
  }
  ```
- **Spaces**: 
  - After keywords: `if (`, `while (`, `return `
  - Around operators: `a + b`, `i = 0`
  - No space before semicolon

### Naming Conventions
- **Functions**: `ft_strlen`, `init_data` (lowercase + underscore)
- **Variables**: `last_meal_time`, `count` (lowercase + underscore)
- **Macros**: `MAX_PHILOS`, `BUFFER_SIZE` (UPPERCASE)
- **Structs**: `struct s_philo` (prefix `s_`)
- **Typedefs**: `t_philo`, `t_data` (prefix `t_`)

### Common Violations
1. **Line too long**: Split at operators or function parameters
2. **Function too long**: Extract logic into helper functions
3. **Too many functions**: Split file into logical modules
4. **Mixed spaces/tabs**: Use tabs only for indentation
5. **Missing newline at EOF**: Add empty line at file end
6. **Multiple newlines**: Remove extra blank lines
7. **Space before semicolon**: Remove space
8. **Forbidden functions**: Use only allowed functions per subject

## Process

1. **Check files**: Run `norminette *.c *.h` or `norminette -R CheckForbiddenSourceHeader`
2. **Read errors**: Identify specific violations and line numbers
3. **Fix violations**: Apply corrections following rules above
4. **Verify**: Re-run norminette to confirm fixes
5. **Common fixes**:
   - Line length → break at logical points
   - Function length → extract subfunctions
   - Formatting → adjust braces/spaces
   - Naming → rename to convention

## Standard 42 Header Template

```c
/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   filename.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: login <login@student.42.fr>                +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: YYYY/MM/DD HH:MM:SS by login            #+#    #+#             */
/*   Updated: YYYY/MM/DD HH:MM:SS by login           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
```

## Quick Fixes

### Line Too Long
```c
// Before (83 chars)
printf("Philosopher %d has taken a fork and is now eating spaghetti\n", id);

// After (split string)
printf("Philosopher %d has taken a fork and is now eating "
    "spaghetti\n", id);
```

### Function Too Long
Extract repeated logic:
```c
// Before: 30-line function
int process_data(t_data *data)
{
    // validation (5 lines)
    // processing (20 lines)
    // cleanup (5 lines)
}

// After: split into helpers
int validate_data(t_data *data);
int process_logic(t_data *data);
int cleanup_data(t_data *data);
```

### Check Command
```bash
# Check all files
norminette

# Check specific files
norminette src/*.c include/*.h

# Ignore header check (for testing)
norminette -R CheckDefine src/main.c
```
