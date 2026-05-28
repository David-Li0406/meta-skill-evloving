## Code Review Guidelines

Review the changes with a focus on (front-end projects as an example):

- Compliance with project coding standards and conventions
- Code quality and best practices
- Clear and correct JSDoc comments
- Type safety and proper TypeScript usage
- React best practices (when applicable)

## Mechanism

Execute code review using 3-tier severity system:

#### 🚨 CRITICAL (Must fix)

- Configuration changes risking outages
- Security vulnerabilities
- Data loss risks
- Breaking changes

#### ⚠️ HIGH PRIORITY (Should fix)

- Performance degradation risks
- Maintainability issues
- Missing error handling

#### 💡 SUGGESTIONS (Consider)

- Code style improvements
- Optimization opportunities
- Additional test coverage
