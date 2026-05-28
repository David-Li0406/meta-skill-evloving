# Atomic Design Classification Rules

Clear decision criteria for categorizing UI patterns from Stitch HTML exports.

## Quick Decision Tree

```
Is it a single HTML element with no children components?
├── YES → ATOM
└── NO → Does it combine 2-5 atoms into one functional unit?
    ├── YES → MOLECULE
    └── NO → ORGANISM
```

---

## Atoms

**Definition:** Smallest indivisible UI units. Cannot be broken down further without losing meaning.

### Criteria
- Single HTML element or simple wrapper
- No composed child components
- Self-contained styling
- Reusable across any context

### Examples
| Atom | Description | shadcn |
|------|-------------|--------|
| Button | Click action | Button |
| Input | Text entry | Input |
| Label | Form label | Label |
| Badge | Status indicator | Badge |
| Icon | Visual symbol | Lucide icons |
| Avatar | Profile image | Avatar |
| Checkbox | Toggle selection | Checkbox |
| Switch | On/off toggle | Switch |
| Separator | Visual divider | Separator |
| Skeleton | Loading placeholder | Skeleton |

### Detection in HTML
Look for elements that:
- Have no nested interactive elements
- Use single semantic tag (`<button>`, `<input>`, `<span>`)
- Repeat frequently with only text/icon changes

---

## Molecules

**Definition:** Groups of atoms functioning together as a unit. One clear purpose.

### Criteria
- Combines 2-5 atoms
- Single functional purpose
- Reusable as a unit
- No internal business logic
- Could exist in multiple contexts

### Examples
| Molecule | Composition | Purpose |
|----------|-------------|---------|
| Form Field | Label + Input + Error | Labeled input with validation |
| Search Bar | Input + Button + Icon | Search functionality |
| Nav Item | Icon + Label + Badge | Navigation entry |
| Stat Card | Number + Label + Trend | Single metric display |
| Avatar Group | Multiple Avatars | Show multiple users |
| Breadcrumb Item | Link + Separator | Navigation path segment |
| Tag Input | Input + Badge(s) | Multi-value entry |
| Menu Item | Icon + Label + Shortcut | Action in menu |

### Detection in HTML
Look for patterns that:
- Contain 2-5 distinct child elements
- Repeat together as a group
- Have shared container styling
- Perform one clear function

### Molecule vs Atom Decision

**If unsure, ask:**
1. Can I use any part independently? → Parts are atoms
2. Does it make sense only as a whole? → It's a molecule
3. Would removing one part break functionality? → Probably molecule

---

## Organisms

**Definition:** Complex UI sections composed of molecules and/or atoms. Major page regions.

### Criteria
- Combines multiple molecules
- Forms distinct page section
- May have internal state (open/closed, selected)
- Represents complete functional area
- Often has own layout concerns

### Examples
| Organism | Composition | Purpose |
|----------|-------------|---------|
| Sidebar | Logo + Nav Items + User Menu | Main navigation |
| Data Table | Headers + Rows + Pagination | Data display with interaction |
| Header Bar | Logo + Search + Nav + User | Page header |
| Settings Panel | Sections + Form Fields + Actions | Configuration |
| Comment Thread | Comments + Reply Forms + Actions | Discussion |
| Dashboard Grid | Multiple Stat Cards + Charts | Overview display |
| Terminal Log | Log Entries + Controls + Filters | Output display |
| Form Section | Heading + Multiple Form Fields + Actions | Form grouping |

### Detection in HTML
Look for sections that:
- Have distinct visual boundaries
- Contain multiple molecule-level patterns
- Would be a "region" in accessibility terms
- Have their own header/title
- Could have internal state

### Organism vs Molecule Decision

**If unsure, ask:**
1. Does it form a complete "section" of the page? → Organism
2. Could it have its own state (expanded, filtered, sorted)? → Organism
3. Is it just atoms working together? → Molecule
4. Would it make sense as a standalone component in Storybook? → Organism

---

## Classification Flowchart

```
START: Analyze HTML pattern
        │
        ▼
┌───────────────────────────────┐
│ Count distinct child elements │
└───────────────────────────────┘
        │
        ▼
   ┌────┴────┐
   │ 0 or 1  │────────────────────────► ATOM
   └────┬────┘
        │
   ┌────┴────┐
   │  2-5    │
   └────┬────┘
        │
        ▼
┌─────────────────────────────────┐
│ Are children atoms OR molecules?│
└─────────────────────────────────┘
        │
   ┌────┴────┐
   │ Atoms   │────────────────────────► MOLECULE
   │  only   │
   └────┬────┘
        │
   ┌────┴────┐
   │Contains │────────────────────────► ORGANISM
   │molecules│
   └─────────┘
        │
        ▼
   ┌────┴────┐
   │  6+     │
   └────┬────┘
        │
        ▼
┌─────────────────────────────────┐
│ Is it a distinct page section?  │
└─────────────────────────────────┘
        │
   ┌────┴────┐      ┌────┴────┐
   │   YES   │──────│   NO    │
   └────┬────┘      └────┬────┘
        │                │
        ▼                ▼
    ORGANISM      Consider splitting
                  into smaller parts
```

---

## Edge Cases

### Icons with Text
- Icon alone → Atom
- Icon + Label → Atom (if single purpose like nav item text)
- Icon + Label + Badge + Action → Molecule

### Cards
- Empty card container → Atom (Card primitive)
- Card with specific content structure → Molecule
- Card grid/collection with interactions → Organism

### Forms
- Single input → Atom
- Input + Label + Error → Molecule (Form Field)
- Multiple form fields + Submit → Organism (Form Section)
- Entire form → Organism

### Tables
- Table header cell → Atom
- Table row → Molecule
- Full table with sort/filter/pagination → Organism

### Navigation
- Single nav link → Atom
- Nav link + Icon + Badge → Molecule
- Full sidebar with sections → Organism

---

## Common Mistakes

### Over-atomizing
**Wrong:** Breaking a search bar into Input atom, Button atom, Icon atom
**Right:** Search Bar is a molecule (atoms function together)

### Under-atomizing
**Wrong:** Calling a button with loading state a molecule
**Right:** Button with states is still an atom (single element)

### Molecule bloat
**Wrong:** 10+ element "molecule"
**Right:** If it has 6+ parts, probably an organism or needs splitting

### Hardcoding classification
**Wrong:** "All cards are molecules"
**Right:** Card shell = atom, Card with fixed structure = molecule, Card grid = organism
