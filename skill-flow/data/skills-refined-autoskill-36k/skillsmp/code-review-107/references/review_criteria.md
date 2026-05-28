# Code Review Criteria

This document defines the comprehensive criteria for reviewing pull requests, organized by category.

## Code Quality & Standards

### Readability & Maintainability
- Code follows established conventions (naming, formatting, indentation)
- Functions and classes have clear, descriptive names
- Code is self-documenting with minimal need for comments
- Complex logic includes explanatory comments
- No commented-out code blocks
- No debug statements (console.log, print) left in production code

### Code Organization
- Single Responsibility Principle followed
- Appropriate abstraction levels
- DRY (Don't Repeat Yourself) - no unnecessary duplication
- Proper separation of concerns
- Logical file and directory structure

### Error Handling
- Appropriate error handling for failure cases
- Meaningful error messages
- No swallowed exceptions
- Proper cleanup in error paths (close files, release resources)

### Testing
- Adequate test coverage for new functionality
- Tests are clear and maintainable
- Edge cases are covered
- Tests actually verify the behavior they claim to test
- No flaky tests

### Performance
- No obvious performance issues
- Appropriate use of algorithms and data structures
- Database queries are optimized (no N+1 queries)
- Proper caching where appropriate
- No memory leaks

## Security

### Input Validation
- All user input is validated (type, format, range, length)
- Input validation happens server-side
- File uploads are restricted by type and size
- Path traversal vulnerabilities prevented

### Injection Prevention
- SQL injection prevented (parameterized queries, ORM)
- Command injection prevented (no unsafe system calls)
- Code injection prevented (no eval, no dynamic code execution)
- XSS prevented (output escaping, CSP headers)
- LDAP/XML injection prevented

### Authentication & Authorization
- Authentication required for protected endpoints
- Authorization checks verify user permissions
- Session management is secure
- Passwords properly hashed (bcrypt, argon2)
- No credentials in code or logs
- Secure password reset flows

### Data Protection
- Sensitive data identified and protected
- Encryption used for sensitive data at rest
- TLS/HTTPS used for data in transit
- Personal information handled per privacy regulations
- Secure random number generation (cryptographically secure)

### API Security
- Rate limiting implemented
- CSRF protection for state-changing operations
- Proper CORS configuration
- API keys/tokens properly validated
- No sensitive data in URLs or logs

## Architecture & Design

### Design Patterns
- Appropriate design patterns used
- SOLID principles followed
- Code is loosely coupled
- Dependencies are injected, not hardcoded
- Interfaces used appropriately

### Integration
- Integrates cleanly with existing codebase
- Consistent with existing architectural patterns
- No unnecessary dependencies introduced
- Backward compatibility maintained (if required)
- Migration path clear for breaking changes

### Scalability
- Solution scales appropriately
- No hardcoded limits that will cause issues
- Asynchronous operations where appropriate
- Proper handling of concurrent access

### Data Model
- Database schema changes are appropriate
- Indexes added where needed
- No redundant data storage
- Proper foreign key relationships
- Migration scripts included

## Alignment with Requirements

### Functional Requirements
- Implements stated requirements completely
- No missing functionality from acceptance criteria
- Behavior matches specifications
- Edge cases from requirements addressed

### Non-Functional Requirements
- Performance requirements met
- Accessibility requirements addressed
- Internationalization/localization considered
- Browser/platform compatibility verified

### User Experience
- UI changes are intuitive
- Error messages are user-friendly
- Loading states handled appropriately
- Responsive design on required devices

## Documentation

### Code Documentation
- Public APIs documented
- Complex algorithms explained
- Non-obvious behavior documented
- TODOs include ticket references

### External Documentation
- README updated if needed
- API documentation updated
- Configuration changes documented
- Deployment notes included if needed

## Review Severity Levels

### Critical (Must Fix)
- Security vulnerabilities
- Data loss or corruption risks
- Breaking changes without migration
- Crashes or unhandled errors
- Production-impacting bugs

### Important (Should Fix)
- Significant code quality issues
- Performance problems
- Missing test coverage for critical paths
- Violations of architectural patterns
- Poor error handling

### Suggestions (Nice to Have)
- Code style improvements
- Refactoring opportunities
- Additional test cases
- Documentation enhancements
- Performance optimizations for non-critical paths
