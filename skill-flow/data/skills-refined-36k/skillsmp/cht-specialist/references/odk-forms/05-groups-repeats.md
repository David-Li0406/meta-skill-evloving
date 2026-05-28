# Groups and Repeats

Organize questions with groups and collect multiple instances with repeats.

## Groups

### Basic Syntax

| type | name | label | appearance |
|------|------|-------|------------|
| begin_group | demographics | Demographics | |
| text | first_name | First Name | |
| text | last_name | Last Name | |
| integer | age | Age | |
| end_group | | | |

### Group Appearances

| Appearance | Description |
|------------|-------------|
| `field-list` | Show all questions on one screen |
| `table-list` | Compact table layout |

### Field-List Example

| type | name | label | appearance |
|------|------|-------|------------|
| begin_group | contact | Contact Info | field-list |
| text | phone | Phone | |
| text | email | Email | |
| text | address | Address | |
| end_group | | | |

### Labeled vs Unlabeled Groups

**Labeled groups** (with `label`):
- Appear in navigation/jump menu
- Show navigation path (e.g., "Demographics > Name")

**Unlabeled groups** (no `label`):
- Invisible organizational structure
- Don't appear in navigation

---

## Nested Groups

Groups can contain other groups. Always close inner groups first.

| type | name | label |
|------|------|-------|
| begin_group | patient | Patient Information |
| begin_group | personal | Personal Details |
| text | first_name | First Name |
| text | last_name | Last Name |
| end_group | | |
| begin_group | medical | Medical History |
| text | conditions | Conditions |
| end_group | | |
| end_group | | |

---

## Conditional Groups

Apply `relevant` to show/hide entire groups:

| type | name | label | relevant |
|------|------|-------|----------|
| select_one yes_no | has_children | Do you have children? | |
| begin_group | children_info | Children Information | ${has_children} = 'yes' |
| integer | num_children | Number of children | |
| text | children_names | Children's names | |
| end_group | | | |

---

## Repeats

Collect multiple instances of data.

### Basic Repeat

| type | name | label |
|------|------|-------|
| begin_repeat | children | Children |
| text | child_name | Child Name |
| integer | child_age | Child Age |
| select_one gender | child_sex | Child Sex |
| end_repeat | | |

### Controlling Repeat Count

| Method | Column | Example |
|--------|--------|---------|
| User-controlled | (default) | Users add/remove |
| Fixed count | `repeat_count` | `3` |
| Dynamic count | `repeat_count` | `${num_children}` |

### Fixed Count Example

| type | name | label | repeat_count |
|------|------|-------|--------------|
| integer | num_items | How many items? | |
| begin_repeat | items | Items | ${num_items} |
| text | item_name | Item Name | |
| end_repeat | | | |

---

## Referencing Repeat Data

### Inside the Same Repeat

Normal references work:
```
${child_age}
${child_name}
```

### Outside the Repeat

Use `indexed-repeat()`:
```
indexed-repeat(${child_name}, ${children}, 1)   # First child's name
indexed-repeat(${child_age}, ${children}, 2)    # Second child's age
```

### Count Instances

```
count(${children})
```

### Aggregate Functions

```
sum(${children}/child_age)      # Sum of all ages
min(${children}/child_age)      # Minimum age
max(${children}/child_age)      # Maximum age
```

### Position in Repeat

Get current 1-based index:
```
position(..)
```

### Example: Numbered Items

| type | name | label |
|------|------|-------|
| begin_repeat | items | Items |
| note | item_num | Item #${position(..)} |
| text | item_name | Item Name |
| end_repeat | | |

---

## Repeat with Summary

Calculate totals outside repeat:

| type | name | label | calculation |
|------|------|-------|-------------|
| begin_repeat | purchases | Purchases | |
| text | item | Item | |
| decimal | price | Price | |
| end_repeat | | | |
| calculate | total | | sum(${purchases}/price) |
| note | total_display | Total: ${total} | |

---

## Sequential Repeats

Collect names first, then ask detailed questions:

| type | name | label | repeat_count |
|------|------|-------|--------------|
| integer | num_people | How many people? | |
| begin_repeat | names | Names | ${num_people} |
| text | person_name | Name | |
| end_repeat | | | |
| begin_repeat | details | Details | count(${names}) |
| note | asking_about | About: indexed-repeat(${person_name}, ${names}, position(..)) | |
| integer | person_age | Age | |
| end_repeat | | | |

---

## Repeat Instance Naming

Make instances identifiable in navigation:

| type | name | label |
|------|------|-------|
| begin_repeat | household_members | Household Members |
| begin_group | member_group | ${first_name} ${last_name} |
| text | first_name | First Name |
| text | last_name | Last Name |
| integer | age | Age |
| end_group | | |
| end_repeat | | |

---

## Limitations

- Cannot nest `field-list` groups inside repeats
- Cannot place repeats inside `field-list` groups
- Performance degrades with many repeat instances
- All repeat data downloaded to device

---

## Multi-Page Forms

Create paginated web forms:

1. Set `style: pages` in settings sheet
2. Apply `field-list` to groups
3. Each `field-list` group becomes a page

### Settings Sheet

| form_title | form_id | style |
|------------|---------|-------|
| Survey | survey | pages |

### Survey Sheet

| type | name | label | appearance |
|------|------|-------|------------|
| begin_group | page1 | Personal Info | field-list |
| text | name | Name | |
| integer | age | Age | |
| end_group | | | |
| begin_group | page2 | Contact Info | field-list |
| text | phone | Phone | |
| text | email | Email | |
| end_group | | | |
