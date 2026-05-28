# Repositories and Unit of Work

## Repositories

- Define interfaces in Application or Domain.
- Implement in Infrastructure.
- Keep methods task-focused (not generic CRUD dumps).

## Unit of Work

- Wrap transactional changes and commit once.
- Use one DbContext instance per unit of work.
