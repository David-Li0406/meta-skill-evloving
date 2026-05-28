# Gravito ADR Reference

## Component Rules

### 1. Models (Atlas)
- Location: `src/models/`
- Rules: Extend `Model`, define `static table`, use `@column`.

### 2. Repositories
- Location: `src/repositories/`
- Rules: Dedicated classes for DB access. No logic, only queries.

### 3. Actions
- Location: `src/actions/[Domain]/`
- Rules: Single Responsibility. One class per use case. Extend `Action<Input, Output>`.

### 4. Controllers
- Location: `src/controllers/api/v[N]/`
- Rules: Thin layer. Use `c.get('parsed_body')` for body caching.

## Directory Layout
```
src/
├── actions/
├── models/
├── repositories/
├── controllers/
└── routes/
```
