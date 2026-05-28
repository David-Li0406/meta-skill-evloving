---
name: webf-native-development
description: Use this skill when developing custom native UI libraries and plugins for WebF, wrapping Flutter widgets and platform capabilities as web-accessible components and APIs.
---

# WebF Native Development

This skill guides the development of custom native UI components and plugins for **WebF** (Web on Flutter). It encompasses creating reusable component libraries that wrap Flutter widgets as web-accessible custom elements and developing native plugins that expose Flutter/platform capabilities as JavaScript APIs.

## Concept

WebF allows you to render HTML/CSS using Flutter's rendering engine. This skill helps you expose complex Flutter widgets as `<custom-element>` tags usable in HTML and wrap Flutter packages or platform capabilities as WebF modules.

## Workflow for Native UI Development

1. **Create Flutter Widget**: Build the widget using standard Flutter code.
2. **Define Element Class**: Create a class extending `WidgetElement`.
3. **Register Custom Element**: Use `defineCustomElement` to map the tag name to the class.

### Example of a Flutter Button Element

```dart
import 'package:webf/webf.dart';
import 'package:flutter/material.dart';

class FlutterButtonElement extends WidgetElement {
  FlutterButtonElement(BindingContext? context) : super(context);

  @override
  Widget build(BuildContext context, List<Widget> children) {
    return ElevatedButton(
      onPressed: () {
        dispatchEvent(Event('click'));
      },
      child: Text(getAttribute('label') ?? 'Click Me'),
    );
  }
}

void main() {
  WebF.defineCustomElement('flutter-button', (context) => FlutterButtonElement(context));
  runApp(MyApp());
}
```

### Usage in HTML

```html
<flutter-button label="Submit Order" id="btn"></flutter-button>
<script>
  document.getElementById('btn').addEventListener('click', () => {
    console.log('Button clicked via Flutter!');
  });
</script>
```

## Workflow for Native Plugin Development

1. **Check for Existing Plugins**: Verify if the required functionality is available in the official WebF plugin registry.
2. **Create Flutter Package**: Build a standard Flutter package that wraps the desired functionality.
3. **Write TypeScript Definitions**: Create `.d.ts` files for the plugin's API.
4. **Generate npm Package**: Use the WebF CLI to generate the npm package and Dart bindings.
5. **Test and Publish**: Ensure the plugin works in both Flutter and JavaScript environments, then publish to pub.dev and npm.

### Example of a Native Plugin

```dart
import 'package:webf/bridge.dart';
import 'package:webf/module.dart';

class MyPluginModule extends BaseModule {
  MyPluginModule(super.moduleManager);

  @override
  Future<String> myAsyncMethod(String input) async {
    // Implementation using Flutter package
  }
}
```

### TypeScript Definitions for the Plugin

```typescript
interface MyPlugin {
  myAsyncMethod(input: string): Promise<string>;
}
```

## Best Practices

- **Attributes**: Map HTML attributes to Widget properties.
- **Events**: Dispatch standard DOM events from Flutter user interactions.
- **Performance**: Avoid heavy computations in the `build` method; use state management.
- **Error Handling**: Return structured error information instead of throwing exceptions to JavaScript.

## Common Patterns

### Handling Complex Properties

```dart
@override
set items(String? value) {
  if (value != null) {
    try {
      _items = jsonDecode(value);
      setState(() {});
    } catch (e) {
      print('Error parsing items: $e');
    }
  }
}
```

### Dispatching Custom Events

```dart
void _handleValueChange(String newValue) {
  dispatchEvent(CustomEvent('change', detail: {'value': newValue}));
}
```

### Lifecycle Management

```dart
@override
void didMount() {
  super.didMount();
  _initializeWidget();
}

@override
void dispose() {
  _debounceTimer?.cancel();
  super.dispose();
}
```

## Resources

- **WebF Documentation**: [Official Documentation](https://openwebf.com/en/docs/developer-guide/native-plugins)
- **CLI Development Guide**: [cli/CLAUDE.md](https://github.com/openwebf/webf/blob/main/cli/CLAUDE.md)
- **Example Plugin**: [native_plugins/share](https://github.com/openwebf/webf/tree/main/native_plugins/share)

## Summary

Use this skill to create both native UI components and plugins for WebF, enabling seamless integration of Flutter's capabilities into web technologies. Follow the outlined workflows and best practices to ensure robust and reusable code.