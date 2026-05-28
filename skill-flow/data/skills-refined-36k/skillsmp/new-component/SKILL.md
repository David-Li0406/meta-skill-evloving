---
name: new-component
description: Create a new ECS component in rogueverse. Use when adding components, creating component classes, or extending the ECS system with new data types.
allowed-tools: Read, Edit, Write, Bash(dart:*), Grep, Glob
---

# New Component Creation Skill

This skill guides you through creating a new ECS component for the rogueverse project, ensuring all patterns and conventions are followed.

## Overview

Creating a new component involves these steps:
1. Add the component class to `lib/ecs/components.dart`
2. Run `build_runner` to generate the mapper
3. Create inspector metadata in `lib/app/widgets/overlays/inspector/sections/`
4. Register the metadata in `properties_panel.dart`
5. Consider if a new System is needed
6. Consider if an Interaction Definition is needed (for player-interactable components)

## Step 1: Component Class Pattern

All components must follow this pattern in `lib/ecs/components.dart`:

### Simple Marker Component (no data):
```dart
/// Brief description of what this marker indicates.
@MappableClass()
class MyMarker with MyMarkerMappable implements Component {
  @override
  String get componentType => "MyMarker";
}
```

### Data Component:
```dart
/// Description of the component's purpose.
@MappableClass()
class MyComponent with MyComponentMappable implements Component {
  final int someValue;
  final String someName;

  MyComponent({required this.someValue, required this.someName});

  @override
  String get componentType => "MyComponent";
}
```

### Intent Component (for player/AI actions):
```dart
/// Description of what action this intent represents.
@MappableClass()
class MyActionIntent extends IntentComponent with MyActionIntentMappable {
  final int targetId;

  MyActionIntent({required this.targetId});

  @override
  String get componentType => "MyActionIntent";
}
```

### Event Component (cleared before/after tick):
```dart
/// Component added when [event description].
@MappableClass()
class DidSomething extends BeforeTick with DidSomethingMappable implements Component {
  final int relevantData;

  DidSomething({required this.relevantData}) : super(1);

  @override
  String get componentType => "DidSomething";
}
```

## Key Rules for Components

1. **Data-only**: Components should only contain data, no behavior/logic
2. **Immutable fields preferred**: Use `final` for fields when possible
3. **Required annotation**: Always use `@MappableClass()` annotation
4. **Mixin naming**: The mixin name is `{ClassName}Mappable`
5. **componentType getter**: Must return the class name as a string
6. **Documentation**: Add a doc comment explaining the component's purpose

## Step 2: Run Build Runner

After adding the component, run:
```bash
dart run build_runner build --delete-conflicting-outputs
```

This generates the `components.mapper.dart` file with serialization code.

## Step 3: Inspector Metadata

Create a metadata class for the inspector UI. Choose the appropriate pattern:

### For Marker Components (no editable fields):

Add to an existing `*_sections.dart` file or create a new one:

```dart
/// Metadata for the MyMarker marker component.
class MyMarkerMetadata extends MarkerComponentMetadata {
  @override
  String get componentName => 'MyMarker';

  @override
  bool hasComponent(Entity entity) => entity.has<MyMarker>();

  @override
  Component createDefault() => MyMarker();

  @override
  void removeComponent(Entity entity) => entity.remove<MyMarker>();
}
```

### For Data Components (with editable fields):

```dart
/// Metadata for the MyComponent component.
class MyComponentMetadata extends ComponentMetadata {
  static const _theme = PropertyPanelThemeData(labelColumnWidth: 140);

  @override
  String get componentName => 'MyComponent';

  @override
  bool hasComponent(Entity entity) => entity.has<MyComponent>();

  @override
  Widget buildContent(Entity entity) {
    return StreamBuilder<Change>(
      stream: entity.parentCell.componentChanges.onEntityOnComponent<MyComponent>(entity.id),
      builder: (context, snapshot) {
        final comp = entity.get<MyComponent>();
        if (comp == null) return const SizedBox.shrink();

        return Column(
          children: [
            PropertyRow(
              key: ValueKey('mycomp_someValue_${comp.someValue}'),
              item: IntPropertyItem(
                id: "someValue",
                label: "Some Value",
                value: comp.someValue,
                onChanged: (int newVal) {
                  entity.upsert<MyComponent>(comp.copyWith(someValue: newVal));
                },
              ),
              theme: _theme,
            ),
            // Add more PropertyRow widgets for each field...
          ],
        );
      },
    );
  }

  @override
  Component createDefault() => MyComponent(someValue: 0, someName: 'default');

  @override
  void removeComponent(Entity entity) => entity.remove<MyComponent>();
}
```

### Property Types Available:
- `IntPropertyItem` - for integers
- `StringPropertyItem` - for strings
- `BoolPropertyItem` - for booleans
- `DoublePropertyItem` - for doubles
- `EnumPropertyItem<T>` - for enums

## Step 4: Register in Inspector

1. If you created a new section file, export it in `sections/sections.dart`:
```dart
export 'my_new_section.dart';
```

2. Register the metadata in `properties_panel.dart`'s `_registerAllComponents()`:
```dart
// Add under appropriate category comment
ComponentRegistry.register(MyComponentMetadata());
```

## Step 5: Consider System Needs

**ASK THE USER** if they need a new System to process this component.

Systems are needed when:
- The component represents an action/intent that needs processing
- The component data needs to be updated each tick
- The component triggers side effects on other entities

Systems are NOT needed for:
- Pure data storage components (like Name, Renderable)
- Marker/tag components that are just checked by other systems

If a System is needed, follow the pattern in `lib/ecs/systems.dart`:

```dart
/// Description of what this system does.
@MappableClass()
class MySystem extends System with MySystemMappable {
  @override
  int get priority => 100; // Default priority

  @override
  void update(World world) {
    Timeline.timeSync("MySystem: update", () {
      final components = world.get<MyComponent>();

      for (final entry in components.entries) {
        final entity = world.getEntity(entry.key);
        // Process entity...
      }
    });
  }
}
```

## Step 6: Consider Interaction Definition

**ASK THE USER** if this component represents something the player can interact with.

The game uses a context menu system for player interactions (triggered by E key or right-click). If the new component represents an interactable entity, you may need to register an `InteractionDefinition` in the interaction registry.

Interaction definitions are needed when:
- The component represents something the player can interact with (doors, items, controls, resources)
- There's already an Intent component for the action (e.g., `OpenIntent`, `PickupIntent`)
- The player needs to be able to trigger this action via the E key or right-click menu

Interaction definitions are NOT needed for:
- Components that are purely internal state
- Actions that happen automatically (e.g., walking into a door auto-opens it)
- AI-only behaviors

### Adding an Interaction Definition

Add to `lib/game/interaction/interaction_registry.dart`:

```dart
InteractionDefinition(
  actionName: 'My Action',      // Display name in menu (e.g., "Open", "Pick up")
  actionVerb: 'Doing action',   // Present participle for feedback
  genericLabel: 'Thing',        // Fallback if entity has no Name component
  range: 1,                     // Manhattan distance: 0=same tile, 1=adjacent
  isAvailable: (e) => e.has<MyComponent>() && /* any state checks */,
  createIntent: (e) => MyActionIntent(targetEntityId: e.id),
),
```

### Key Fields:
- **actionName**: What appears in the context menu
- **genericLabel**: Fallback entity name (e.g., "Door", "Item", "Resource")
- **range**: How far the player can be to interact
  - `0` = must be on the same tile (pickup, take control)
  - `1` = adjacent tiles (open door, mine)
  - `N` = up to N tiles away (ranged interactions)
- **isAvailable**: Function that checks if interaction is valid for this entity
- **createIntent**: Function that creates the Intent component to execute

### Related Files:
- `lib/game/interaction/interaction_definition.dart` - InteractionDefinition class
- `lib/game/interaction/interaction_registry.dart` - Register new interactions here
- `lib/game/interaction/nearby_entity_finder.dart` - Finds interactable entities
- `lib/app/widgets/overlays/interaction_context_menu.dart` - The UI widget

## File Locations Summary

| Type | Location |
|------|----------|
| Component class | `lib/ecs/components.dart` |
| Generated mapper | `lib/ecs/components.mapper.dart` (auto-generated) |
| Inspector metadata | `lib/app/widgets/overlays/inspector/sections/*.dart` |
| Sections barrel | `lib/app/widgets/overlays/inspector/sections/sections.dart` |
| Registry calls | `lib/app/widgets/panels/properties_panel.dart` |
| Systems | `lib/ecs/systems.dart` |
| Interaction registry | `lib/game/interaction/interaction_registry.dart` |

## Workflow Checklist

When creating a new component:

- [ ] Define the component class with `@MappableClass()` annotation
- [ ] Add `with {Name}Mappable implements Component`
- [ ] Implement `componentType` getter
- [ ] Add constructor with appropriate fields
- [ ] Run `dart run build_runner build --delete-conflicting-outputs`
- [ ] Create inspector metadata class (marker or data pattern)
- [ ] Export in `sections/sections.dart` if new file created
- [ ] Register in `properties_panel.dart` `_registerAllComponents()`
- [ ] Ask user if a System is needed for this component
- [ ] Ask user if an Interaction Definition is needed (for player-interactable components)
