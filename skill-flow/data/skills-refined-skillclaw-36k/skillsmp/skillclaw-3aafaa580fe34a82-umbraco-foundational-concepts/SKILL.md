---
name: umbraco-foundational-concepts
description: Use this skill to understand and implement foundational concepts in Umbraco backoffice, including conditions and state management.
---

# Skill body

## What is it?
This skill covers foundational concepts in Umbraco backoffice, focusing on extension conditions and state management. Conditions control the visibility of extensions based on context, while state management allows for reactive data handling across components.

## Documentation
Always fetch the latest docs before implementing:

- **Extension Conditions**: [Main docs](https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-conditions)
- **State Management**: [Main docs](https://docs.umbraco.com/umbraco-cms/customizing/foundation/states)

## Workflow for Extension Conditions

1. **Fetch docs** - Use WebFetch on the URLs above.
2. **Ask questions** - What restricts visibility? Section? Workspace? User? Content type?
3. **Generate code** - Add conditions to manifest based on latest docs.
4. **Explain** - Show what was created and when the extension appears.

### Minimal Examples for Conditions

#### Section Condition
```json
{
  "type": "dashboard",
  "alias": "My.Dashboard",
  "name": "My Dashboard",
  "conditions": [
    {
      "alias": "Umb.Condition.SectionAlias",
      "match": "Umb.Section.Content"
    }
  ]
}
```

#### Workspace Condition
```json
{
  "type": "workspaceView",
  "alias": "My.WorkspaceView",
  "name": "My Workspace View",
  "conditions": [
    {
      "alias": "Umb.Condition.WorkspaceAlias",
      "match": "Umb.Workspace.Document"
    }
  ]
}
```

## Workflow for State Management

1. **Fetch docs** - Use WebFetch on the URLs above.
2. **Ask questions** - What type of state? Who observes? Where to provide observable?
3. **Generate code** - Implement state with observables based on latest docs.
4. **Explain** - Show what was created and how observation works.

### Minimal Examples for State Management

#### Basic State Usage
```typescript
import { UmbStringState } from '@umbraco-cms/backoffice/observable-api';

// Create a state with initial value
const myState = new UmbStringState('initial value');

// Create an observable from the state
const myObservable = myState.asObservable();

// Observe the state (fires immediately and on changes)
this.observe(myObservable, (value) => {
  console.log('Current value:', value);
});

// Update the state (all observers notified)
myState.setValue('updated value');
```

#### State in Context Pattern
```typescript
import { UmbContextBase } from '@umbraco-cms/backoffice/class-api';
import { UmbNumberState } from '@umbraco-cms/backoffice/observable-api';

export class MyContext extends UmbContextBase<MyContext> {
  // Private state
  #counter = new UmbNumberState(0);

  // Public observable (readonly)
  readonly counter = this.#counter.asObservable();

  increment() {
    this.#counter.setValue(this.#counter.getValue() + 1);
  }

  decrement() {
    this.#counter.setValue(this.#counter.getValue() - 1);
  }
}
```