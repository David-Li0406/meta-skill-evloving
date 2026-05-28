# Database Comment Annotations (Codegen Plugin)

This document lists custom annotations parsed from table/column comments and how they affect code generation.

## Syntax

- Annotations are read from table/column comments.
- Format: `@Name` or `@Name=value` (value ends at the next `;` if present).
- Name is `[A-Za-z]+`. Multiple annotations can appear in one comment.
- Annotation tokens are stripped from the comment text used in generated Javadoc.

Example (MySQL):

```sql
COMMENT 'Order status @Type=OrderStatus; @Enum=0:NEW:New|1:PAID:Paid;'
```

## Table-level annotations

| Annotation (aliases)                     | Value                 | Effect                                                                                                                                                  |
|------------------------------------------|-----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| `@Ignore` (`@I`)                         | none                  | Skip this table in entity/enum/schema/spec/factory/domain-event/repository generation and relation discovery.                                           |
| `@Relation` (`@Rel`)                     | none                  | Mark table as a relation (join) table for many-to-many. The table itself is not generated as an entity; columns with `@Reference` define the two sides. |
| `@Parent` (`@P`)                         | parent table name     | Mark as child of the parent table. Used to infer one-to-many/many-to-one links and to decide aggregate root.                                            |
| `@AggregateRoot` (`@Root`, `@R`)         | none                  | Force this table to be treated as aggregate root even if `@Parent` is present.                                                                          |
| `@ValueObject` (`@VO`)                   | none                  | Generate a ValueObject entity (implements `ValueObject`, uses value-object id generator, `Aggregate.TYPE_VALUE_OBJECT`).                                |
| `@Module` (`@M`)                         | module name           | Override module segment used in package path for this table and its descendants.                                                                        |
| `@Aggregate` (`@A`)                      | aggregate name        | Override aggregate name used in package path and metadata.                                                                                              |
| `@Type` (`@T`)                           | entity type           | Override entity class name for this table.                                                                                                              |
| `@Factory` (`@Fac`)                      | none                  | When `generateAggregate=true`, only tables with this annotation generate `*Factory`.                                                                    |
| `@Specification` (`@Spec`, `@Spe`)       | none                  | When `generateAggregate=true`, only tables with this annotation generate `*Specification`.                                                              |
| `@DomainEvent` (`@DE`, `@Event`, `@Evt`) | `Name                 | Name2`                                                                                                                                                  | For aggregate roots, generate domain event base classes and subscribers. Only the segment before `:` is used for class names; `DomainEvent` suffix is added if missing. |
| `@IdGenerator` (`@IG`)                   | generator FQN or name | Use custom id generator for single-PK entities (`@GeneratedValue(generator=...)` + `@GenericGenerator`).                                                |
| `@Lazy` (`@L`)                           | `true/false` or `0/1` | Default fetch type for relations. `true` or `0` => LAZY, `false` or `1` => EAGER, else uses global `fetchType`.                                         |
| `@Count` (`@C`)                          | `one` or `1`          | If a one-to-many targets this table, generator adds `load<Child>()` helper that returns the first element.                                              |

## Column-level annotations

| Annotation (aliases)    | Value                 | Effect                                                                                                                                      |
|-------------------------|-----------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| `@Ignore` (`@I`)        | none                  | Skip this column in entity/schema/enum generation.                                                                                          |
| `@Type` (`@T`)          | Kotlin type           | Override field type. Also adds `@Convert(converter = <Type>.Converter::class)` and imports mapped type.                                     |
| `@Enum` (`@E`)          | enum config           | Declare enum values. Used to generate enum + translation. Use with `@Type` to set enum class name. See "Enum config".                       |
| `@IgnoreInsert` (`@II`) | none                  | `@Column(insertable = false)` for this field.                                                                                               |
| `@IgnoreUpdate` (`@IU`) | none                  | `@Column(updatable = false)` for this field.                                                                                                |
| `@ReadOnly` (`@RO`)     | none                  | `@Column(insertable = false, updatable = false)` for this field.                                                                            |
| `@Reference` (`@Ref`)   | target table          | Reference target table for relation discovery. If empty, inferred from column name by trimming `_id` or `id`.                               |
| `@Relation` (`@Rel`)    | relation type         | Explicit relation type for this column: `OneToOne` / `1:1`, `ManyToOne` / `*:1`. Defaults to `ManyToOne` when only `@Reference` is present. |
| `@Lazy` (`@L`)          | `true/false` or `0/1` | Per-column fetch type override for relations (same mapping as table-level).                                                                 |

## Enum config

Format for `@Enum` value (items separated by `|`):

- `VALUE:NAME:DESC` -> numeric VALUE, NAME, DESC.
- `VALUE:NAME` -> numeric VALUE, NAME, DESC = NAME.
- `NAME:DESC` -> VALUE = 0-based index, NAME, DESC.
- `NAME` -> VALUE = 0-based index, NAME, DESC = NAME.

Example:

```
@Type=OrderStatus; @Enum=0:NEW:New|1:PAID:Paid|2:SHIPPED:Shipped
```
