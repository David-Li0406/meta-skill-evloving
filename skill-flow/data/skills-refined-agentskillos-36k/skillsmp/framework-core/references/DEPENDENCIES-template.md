# Dependency Matrix

Deltas listed in rows depend on deltas in columns.
Mark with `X` where row depends on column.

## Full Dependency Matrix

|           | CAT1-001 | CAT1-002 | CAT2-001 | CAT2-002 |
|-----------|----------|----------|----------|----------|
| CAT1-001  | -        |          |          |          |
| CAT1-002  | X        | -        |          |          |
| CAT2-001  | X        |          | -        |          |
| CAT2-002  |          |          | X        | -        |
