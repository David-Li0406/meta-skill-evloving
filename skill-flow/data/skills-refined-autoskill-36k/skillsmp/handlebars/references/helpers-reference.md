# Handlebars Helpers Reference

This document provides a quick reference to all Handlebars helpers available in Aurora CLI.

## Helper Files Location

All helpers are located in: `src/@cliter/handlebars/helpers/`

## String Transformation

| Helper | File | Description |
|--------|------|-------------|
| `toCamelCase` | `string-to-camel-case.ts` | Convert string to camelCase |
| `toPascalCase` | `string-to-pascal-case.ts` | Convert string to PascalCase |
| `toKebabCase` | `string-to-kebab-case.ts` | Convert string to kebab-case |
| `toSnakeCase` | `string-to-snake-case.ts` | Convert string to snake_case |
| `sumStrings` | `sum-strings.ts` | Concatenate multiple strings |
| `singleLine` | `single-line.ts` | Remove line breaks |
| `replaceI18n` | `replace-i18n.ts` | Replace i18n placeholders |

## Variable Management

| Helper | File | Description |
|--------|------|-------------|
| `setVar` | `set-var.ts` | Set variable in root context |
| `array` | `array.ts` | Create array from arguments |
| `object` | `object.ts` | Create object from key-value pairs |
| `push` | `push.ts` | Push item to array |

## Conditional Helpers

| Helper | File | Description |
|--------|------|-------------|
| `ternary` | `ternary.ts` | Ternary operator |
| `isUndefined` | `is-undefined.ts` | Check if value is undefined |
| `notInArray` | `not-in-array.ts` | Check if value not in array |
| `hasItems` | `has-items.ts` | Check if array has items |

## Loop Helpers

| Helper | File | Description |
|--------|------|-------------|
| `loops` | `loops.ts` | Loop N times with @index, @first, @last |

## ID Generation

| Helper | File | Description |
|--------|------|-------------|
| `uuid` | `uuid.ts` | Generate deterministic UUID |
| `nanoid` | `nanoid.ts` | Generate NanoID |
| `randomIntegerDigits` | `random-integer-digits.ts` | Random integer with N digits |
| `randomDecimalDigits` | `random-decimal-digits.ts` | Random decimal number |

## Property Filters

| Helper | File | Description |
|--------|------|-------------|
| `getEnumProperties` | `get-enum-properties.ts` | Get ENUM type properties |
| `getBooleanProperties` | `get-boolean-properties.ts` | Get BOOLEAN type properties |
| `getTimestampProperties` | `get-timestamp-properties.ts` | Get TIMESTAMP properties |
| `getWithoutTimestampsProperties` | `get-without-timestamps-properties.ts` | Exclude timestamp properties |
| `getWithoutDeletedAtProperties` | `get-without-delete-at-properties.ts` | Exclude deletedAt property |
| `getPrimaryKeyProperties` | `get-primary-key-properties.ts` | Get primary key properties |
| `getNotNullableProperties` | `get-not-nullable-properties.ts` | Get required properties |
| `getIndexesProperties` | `get-indexes-properties.ts` | Get indexed properties |

## Relationship Helpers

| Helper | File | Description |
|--------|------|-------------|
| `getWithRelationshipOneToOneProperties` | `get-with-relationship-one-to-one-properties.ts` | ONE_TO_ONE relations |
| `getWithRelationshipOneToManyProperties` | `get-with-relationship-one-to-many-properties.ts` | ONE_TO_MANY relations |
| `getWithRelationshipManyToOneProperties` | `get-with-relationship-many-to-one-properties.ts` | MANY_TO_ONE relations |
| `getManyToManyRelationshipProperties` | `get-many-to-many-relationship-properties.ts` | MANY_TO_MANY relations |
| `isRelationshipProperty` | `is-relationship-property.ts` | Check if property is relationship |
| `getAggregateNameFromPropertyRelationship` | `get-aggregate-name-from-property-relationship.ts` | Get aggregate name from relation |
| `getModuleNameFromPropertyRelationship` | `get-module-name-from-property-relationship.ts` | Get module name from relation |

## Type Conversion

| Helper | File | Description |
|--------|------|-------------|
| `getDtoTypeProperty` | `get-dto-type-property.ts` | Get DTO TypeScript type |
| `getGraphqlTypeProperty` | `get-graphql-type-property.ts` | Get GraphQL type |
| `getSwaggerTypeProperty` | `get-swagger-type-property.ts` | Get Swagger/OpenAPI type |
| `getPropertySequelizeType` | `get-property-sequelize-type.ts` | Get Sequelize type |
| `getJavascriptModelTypeProperty` | `get-javascript-model-type-property.ts` | Get JS model type |

## Import/Code Generation

| Helper | File | Description |
|--------|------|-------------|
| `importManager` | `import-manager.ts` | Generate import statements |
| `constructorInjectorManager` | `constructor-injector-manager.ts` | Generate constructor injections |
| `variablesInjectorManager` | `variables-injector-manager.ts` | Generate variable declarations |
| `returnTypeManager` | `return-type-manager.ts` | Generate return type |

## Validation Helpers

| Helper | File | Description |
|--------|------|-------------|
| `isAllowProperty` | `is-allow-property.ts` | Check if property is allowed |
| `isAllowPath` | `is-allow-path.ts` | Check if path is allowed |
| `hasValidationFormControl` | `has-validation-form-control.ts` | Check validation rules |

## i18n Helpers

| Helper | File | Description |
|--------|------|-------------|
| `hasI18nProperties` | `has-i18n-properties.ts` | Check for i18n properties |
| `getI18nProperties` | `get-i18n-properties.ts` | Get i18n properties |
| `isI18nRelationProperty` | `is-i18n-relation-property.ts` | Check i18n relation |
| `isI18nAvailableLangsProperty` | `is-i18n-available-langs-property.ts` | Check available langs |

## Bracket Helpers

| Helper | File | Description |
|--------|------|-------------|
| `bracketOpen` | `bracket-open.ts` | Output `{` character |
| `bracketClose` | `bracket-close.ts` | Output `}` character |

## Partials Location

All partials are in: `src/@cliter/handlebars/partials/`

| Partial | File | Description |
|---------|------|-------------|
| `i18n` | `i18n.ts` | i18n property handling |
| Inputs | `inputs/*.ts` | Form input partials |
| Relationships | `relationships/*.ts` | Relationship component partials |
