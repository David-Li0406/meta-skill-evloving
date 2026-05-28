---
name: pr-reviewer
description: Expert Flutter PR reviewer for code quality, architecture, performance, and best practices. Use when reviewing pull requests, performing code audits, or ensuring Flutter/Dart code meets production standards.
allowed-tools: Read, Grep, Glob, Bash
---

# Flutter PR Review Skill

Expert code review assistance for Flutter pull requests, focusing on code quality, architecture patterns, performance, and Flutter/Dart best practices.

## When to Use This Skill

- Reviewing pull requests in Flutter projects
- Performing code audits on Flutter/Dart code
- Checking adherence to project coding standards
- Identifying potential bugs, performance issues, or security concerns
- Ensuring consistent code style and architecture

## Review Process

### 1. Initial Assessment
Before diving into details, understand the scope:
- What feature/fix does this PR implement?
- How many files are changed?
- What areas of the codebase are affected?

### 2. Review Checklist

#### Code Quality
- [ ] Code follows Dart style guide and project conventions
- [ ] No unused imports, variables, or dead code
- [ ] Meaningful variable and function names
- [ ] Appropriate use of `const` constructors
- [ ] Proper null safety handling (no unnecessary `!` operators)
- [ ] No hardcoded strings (use LocaleKeys for user-facing text)

#### Architecture & Design
- [ ] Follows clean architecture (data/domain/presentation separation)
- [ ] Business logic separated from UI code
- [ ] Proper dependency injection patterns
- [ ] Single responsibility principle followed
- [ ] No circular dependencies

#### Flutter Specifics
- [ ] Widgets are properly composed (not too large)
- [ ] StatelessWidget used where possible (StatefulWidget only when needed)
- [ ] Proper widget keys used for lists and animations
- [ ] No unnecessary widget rebuilds
- [ ] Responsive design considerations

#### State Management
- [ ] State management follows project patterns (Riverpod/BLoC)
- [ ] State is properly scoped (not too global, not too local)
- [ ] Side effects handled appropriately
- [ ] Loading/error states handled

#### Performance
- [ ] ListView.builder used for long lists
- [ ] Images optimized and cached
- [ ] No expensive operations in build methods
- [ ] Async operations properly handled
- [ ] Memory leaks avoided (dispose called, subscriptions cancelled)

#### Security
- [ ] Sensitive data stored securely (flutter_secure_storage)
- [ ] No hardcoded API keys or secrets
- [ ] User input validated and sanitized
- [ ] No SQL injection or XSS vulnerabilities

#### Data Handling
- [ ] Freezed used for data models
- [ ] Dio used for HTTP requests (not http package)
- [ ] Hive used for caching (non-sensitive data)
- [ ] flutter_secure_storage for sensitive data
- [ ] Proper error handling for network calls

#### Testing
- [ ] Unit tests for business logic
- [ ] Widget tests for UI components
- [ ] Edge cases covered
- [ ] Mocks used appropriately

### 3. Review Commands

```bash
# Get list of changed files
git diff --name-only origin/main...HEAD

# Get detailed diff
git diff origin/main...HEAD

# Check for lint issues
flutter analyze

# Run tests
flutter test

# Check test coverage
flutter test --coverage
```

## Review Response Format

When providing review feedback, use this structure:

### Summary
Brief overview of the PR and overall assessment.

### Critical Issues
Issues that must be fixed before merging:
- **[CRITICAL]** Description of blocking issue
  - File: `path/to/file.dart:line`
  - Suggestion: How to fix

### Improvements
Suggested changes that would improve code quality:
- **[SUGGESTION]** Description
  - File: `path/to/file.dart:line`
  - Why: Explanation
  - Suggestion: How to improve

### Nitpicks
Minor style or preference issues:
- **[NIT]** Description
  - File: `path/to/file.dart:line`

### Positive Feedback
Highlight good practices observed:
- Good use of const constructors in `WidgetName`
- Clean separation of concerns in feature module

## Common Flutter Anti-Patterns to Watch For

### 1. God Widgets
```dart
// Bad: One widget doing everything
class HomePage extends StatefulWidget {
  // 500+ lines of code
}

// Good: Composed smaller widgets
class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        const HomeHeader(),
        const HomeContent(),
        const HomeFooter(),
      ],
    );
  }
}
```

### 2. Business Logic in Widgets
```dart
// Bad: Logic in widget
class UserProfile extends StatelessWidget {
  String formatName(String first, String last) => '$first $last';

  @override
  Widget build(BuildContext context) {
    final name = formatName(user.firstName, user.lastName);
    // ...
  }
}

// Good: Logic in separate class/extension
extension UserExtension on User {
  String get fullName => '$firstName $lastName';
}
```

### 3. Missing Error Handling
```dart
// Bad: No error handling
Future<void> fetchData() async {
  final response = await dio.get('/api/data');
  setState(() => data = response.data);
}

// Good: Proper error handling
Future<void> fetchData() async {
  try {
    final response = await dio.get('/api/data');
    if (mounted) {
      setState(() => data = response.data);
    }
  } on DioException catch (e) {
    // Handle error appropriately
  }
}
```

### 4. Hardcoded Strings
```dart
// Bad: Hardcoded strings
Text('Welcome to our app')

// Good: Use LocaleKeys
Text(LocaleKeys.home_welcome.tr())
```

### 5. Improper Async in initState
```dart
// Bad: Direct async in initState
@override
void initState() {
  super.initState();
  await fetchData(); // Error: can't await in initState
}

// Good: Separate async method
@override
void initState() {
  super.initState();
  _loadData();
}

Future<void> _loadData() async {
  await fetchData();
}
```

### 6. Not Using const
```dart
// Bad: Missing const
return Container(
  padding: EdgeInsets.all(16),
  child: Text('Hello'),
);

// Good: Using const where possible
return Container(
  padding: const EdgeInsets.all(16),
  child: const Text('Hello'),
);
```

## Security Review Points

### Authentication & Authorization
- Check token storage (must use flutter_secure_storage)
- Verify token refresh logic
- Check permission handling

### Data Protection
- Sensitive data encrypted at rest
- Secure communication (HTTPS only)
- No logging of sensitive information

### Input Validation
- Form inputs validated
- API responses validated
- File uploads checked

## Performance Review Points

### Widget Optimization
- Const constructors used
- RepaintBoundary for heavy custom painters
- AutomaticKeepAliveClientMixin for tab content

### List Performance
- ListView.builder for dynamic lists
- Proper itemExtent for fixed-height items
- Pagination for large datasets

### Image Optimization
- Cached network images
- Proper image sizing
- WebP format when possible

### Memory Management
- Dispose controllers and subscriptions
- Avoid holding references in closures
- Use weak references where appropriate

## Review Etiquette

1. **Be Constructive**: Frame feedback as suggestions, not criticisms
2. **Explain Why**: Don't just say what to change, explain the reasoning
3. **Prioritize**: Distinguish between blocking issues and nice-to-haves
4. **Acknowledge Good Work**: Highlight positive aspects
5. **Be Specific**: Reference exact file and line numbers
6. **Suggest Solutions**: Provide code examples when helpful

## Notes

This skill focuses on Flutter-specific review concerns. For state management specifics (Riverpod/BLoC), refer to the dedicated state management skills for deeper review of those patterns.
