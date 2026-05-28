# Common Errors Reference

Troubleshooting guide for common XLSForm errors and their solutions.

## Parse Errors (Before Conversion)

### Error: "Unknown question type"

**Cause:** Invalid question type in `type` column.

**Example:**
```
| type | name |
| number | age |  ← "number" is not valid
```

**Solution:**
- Use `integer` for whole numbers
- Use `decimal` for decimals
- Check [question-types.md](question-types.md) for valid types

**Correct:**
```
| type | name |
| integer | age |
```

---

### Error: "Question name not unique"

**Cause:** Duplicate question names.

**Example:**
```
| name |
| age |
| age |  ← Duplicate!
```

**Solution:**
- Rename one to be unique
- Check spelling (names are case-sensitive)

**Correct:**
```
| name |
| age |
| respondent_age |  ← Different name
```

---

### Error: "Invalid character in name"

**Cause:** Question name has invalid characters.

**Example:**
```
| name |
| respondent-name |  ← Hyphen not allowed
| respondent name  |  ← Space not allowed
| 2age             |  ← Can't start with number
```

**Solution:**
- Use only: letters, numbers, underscore
- Must start with letter or underscore
- Examples: `respondent_name`, `age_2`, `_internal`

**Correct:**
```
| name |
| respondent_name |
| age_group |
| _hidden |
```

---

### Error: "type requires parameter"

**Cause:** `select_one` or `select_multiple` without list name.

**Example:**
```
| type | name |
| select_one | q1 |  ← Missing list name
```

**Solution:**
- Add list name: `select_one list_name`

**Correct:**
```
| type | name |
| select_one yes_no | q1 |
```

---

### Error: "Choice list not found"

**Cause:** `list_name` in survey doesn't match choices worksheet.

**Example:**
Survey:
```
| type | name |
| select_one gender | q1 |
```

Choices (wrong name):
```
| list_name |
| genders |  ← Should be "gender"
```

**Solution:**
- Match exactly (case-sensitive)
- `select_one gender` → `list_name gender`

**Correct:**
```
Choices:
| list_name |
| gender |
```

---

## Validation Errors (During Constraint Check)

### Error: "Constraint failed"

**Cause:** User input doesn't satisfy constraint expression.

**Example:**
```
| constraint | constraint_message |
| . >= 0 and . <= 100 | Must be 0-100 |

User enters: 150
Error: "Must be 0-100"
```

**Solution:**
- Check constraint logic
- Verify input is reasonable
- Loosen constraint if too strict

---

### Error: "Required field empty"

**Cause:** Field marked `required: yes` but left empty.

**Example:**
```
| required |
| yes |

User: Leaves field empty
Error: Required field
```

**Solution:**
- User must enter value
- Or change `required: no` if truly optional

---

## Expression Errors

### Error: "Unknown variable"

**Cause:** Reference to non-existent question.

**Example:**
```
relevant: ${respondent_age} >= 18
(No question named "respondent_age")
```

**Solution:**
- Check variable name spelling (case-sensitive)
- Verify question exists in survey sheet
- Match exactly: `${name}`

**Correct:**
```
relevant: ${age} >= 18
(If question is named "age")
```

---

### Error: "Invalid expression syntax"

**Cause:** Malformed XPath expression.

**Common mistakes:**

1. **Missing quotes on text:**
```
✗ relevant: ${country} = Kenya
✓ relevant: ${country} = 'Kenya'
```

2. **Wrong operator:**
```
✗ relevant: ${country} = ${selected_country}
✓ relevant: ${country} = 'Kenya'
```

3. **Missing parentheses:**
```
✗ if(${age} > 18, 'adult', 'minor')
✓ if(${age} > 18, 'adult', 'minor')
```

---

### Error: "Division by zero"

**Cause:** Calculating a/b where b=0.

**Example:**
```
calculation: ${total} / ${count}
(If count = 0, error)
```

**Solution:**
- Use conditional to check denominator
```
calculation: if(${count} > 0, ${total} / ${count}, 0)
```

---

## Reference Errors

### Error: "Field referenced doesn't exist"

**Cause:** Calculation/constraint references non-existent field.

**Example:**
```
relevant: ${has_children} = 'yes'
(No question named "has_children")
```

**Solution:**
- Verify question exists
- Check spelling and case
- Use exact name from survey sheet

---

### Error: "Circular dependency"

**Cause:** Question A references B, B references A.

**Example:**
```
Question A relevant: ${B} > 0
Question B relevant: ${A} > 0
(A depends on B, B depends on A)
```

**Solution:**
- Remove circular reference
- Redesign logic

---

## Choice Errors

### Error: "Duplicate choice names"

**Cause:** Same choice `name` appears twice in same list.

**Example:**
```
| list_name | name |
| gender | m |
| gender | m |  ← Duplicate!
```

**Solution:**
- Ensure unique names per list
- Rename duplicates

**Correct:**
```
| list_name | name |
| gender | male |
| gender | female |
```

---

### Error: "Choice filter returns no results"

**Cause:** `choice_filter` expression returns nothing.

**Example:**
```
Cascade:
| type | name | choice_filter |
| select_one province | province | province in ${country} |

Choices:
| list_name | name | country |
| province | nairobi | ke |

User selects country: "USA"
Result: No provinces show (USA not in choices)
```

**Solution:**
- Verify filter values match chosen values
- Check column name in choices
- Test all branches

---

## Calculation Errors

### Error: "Type mismatch"

**Cause:** Calculating incompatible types.

**Example:**
```
calculation: ${text_field} + 10
(Can't add number to text)
```

**Solution:**
- Use only compatible types
- Convert if needed: `int(${value})`

---

### Error: "Function not found"

**Cause:** Typo in function name.

**Common mistakes:**
```
✗ TODAY()  (wrong case)
✓ today()  (correct)

✗ Sum(${a}, ${b})  (wrong case)
✓ sum(${a}, ${b})  (correct)

✗ TODAY  (missing parentheses)
✓ today()  (correct)
```

---

## Submission Errors

### Error: "Form submission failed"

**Cause:** Server-side issue (usually after conversion works).

**Solution:**
- Check server configuration
- Verify form ID and version
- Check internet connection
- Review server logs

---

### Error: "File too large"

**Cause:** Form + media files exceed platform limit.

**Example limit:** 50MB for some platforms.

**Solution:**
- Remove embedded media
- Use `select_one_from_file` for large lists
- Split very large forms

---

## Pre-Flight Checklist

Use `validate_xlsform.py` to catch errors:

```bash
python scripts/validate_xlsform.py form.xlsx
```

Checks:
- ✓ Valid question types
- ✓ Unique names
- ✓ Valid characters in names
- ✓ Choice list references
- ✓ Required columns present
- ✓ No obvious syntax errors

---

## Conversion Errors

### Error: "XML parsing failed"

**Cause:** Generated XForm XML is malformed.

**Solution:**
1. Run `validate_xlsform.py` first
2. Fix any validation errors
3. Try conversion again
4. Check pyxform version compatibility

---

## Testing Process

**Before reporting error:**

1. Run validation:
   ```bash
   python scripts/validate_xlsform.py form.xlsx
   ```

2. Fix validation errors first

3. Try conversion:
   ```bash
   python scripts/convert_to_xform.py form.xlsx
   ```

4. Check error message carefully

5. Search common errors above

6. Test on actual device if possible

---

## Getting Help

**Provide:**
- Exact error message
- Which column/row has error
- What you're trying to do
- Expected vs actual behavior

**Helpful example:**
```
Error: "Unknown variable in relevant column, row 12"
Question name: "num_children"
relevant: ${has_children} = 'yes'
No question named has_children exists
Fix: Change to ${has_children} (actual name is "has_children")
```

**Unhelpful example:**
```
"Form not working"
```

---

## See Also

- [validate_xlsform.py](../scripts/validate_xlsform.py) - Automated validation
- [examples.md](../examples.md) - Working forms as reference
- [xpath-expressions.md](xpath-expressions.md) - Expression syntax
- [best-practices.md](best-practices.md) - Preventing errors through good design
