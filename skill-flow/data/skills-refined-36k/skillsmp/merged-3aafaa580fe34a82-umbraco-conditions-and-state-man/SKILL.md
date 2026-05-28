---
name: umbraco-conditions-and-state-management
description: Use this skill to understand and implement conditions and state management in the Umbraco backoffice.
---

# Umbraco Conditions and State Management

## What is it?
This skill encompasses the foundational concepts of both conditions and state management in Umbraco. Conditions control the visibility of extensions based on specific criteria, while state management allows for reactive data sharing across components using the Observable pattern.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs for Conditions**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-conditions
- **Main docs for State Management**: https://docs.umbraco.com/umbraco-cms/customizing/foundation/states
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Context API**: https://docs.umbraco.com/umbraco-cms/customizing/foundation/context-api

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above.
2. **Ask questions** - What restricts visibility for conditions? What type of state is needed?
3. **Generate code** - Implement conditions and states based on the latest docs.
4. **Explain** - Show what was created and how it functions.

## Umbraco Conditions

### Key Concepts
- **Gatekeeping**: Conditions control extension availability.
- **AND Logic**: All conditions must pass for an extension to appear.
- **Match Property**: Value to compare against (alias, entity type, etc.).

### Minimal Examples

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

#### User Permission Condition
```json
{
  "type": "entityAction",
  "alias": "My.DeleteAction",
  "name": "Delete Document",
  "conditions": [
    {
      "alias": "Umb.Condition.UserPermission.Document",
      "match": "Umb.UserPermission.Document.Delete"
    }
  ]
}
```

## Umbraco State Management

### Key Concepts
- **State**: Container for a value (private, mutable).
- **Observable**: Subscription hook created from state (public, readonly).
- **Observer**: Function that reacts to state changes via `observe()`.

### Minimal Examples

#### Basic State Usage
```typescript
import { UmbStringState } from '@umbraco-cms/backoffice/observable-api';

const myState = new UmbStringState('initial value');
const myObservable = myState.asObservable();

this.observe(myObservable, (value) => {
  console.log('Current value:', value);
});

myState.setValue('updated value');
```

#### Complete Context Example
```typescript
import { UmbContextBase } from '@umbraco-cms/backoffice/class-api';
import { UmbStringState, UmbArrayState } from '@umbraco-cms/backoffice/observable-api';

export class TodoContext extends UmbContextBase<TodoContext> {
  #title = new UmbStringState('My Todo List');
  #todos = new UmbArrayState<string>([]);

  readonly title = this.#title.asObservable();
  readonly todos = this.#todos.asObservable();

  setTitle(value: string) {
    this.#title.setValue(value);
  }

  addTodo(todo: string) {
    this.#todos.setValue([...this.#todos.getValue(), todo]);
  }
}
```

## Use Cases
- Show dashboard only in specific sections.
- Share data between contexts and elements.
- Restrict features based on user permissions.
- Enable reactive UI updates across components.

That's it! Always fetch fresh docs, keep examples minimal, and generate complete working code.