# Naming Conventions

Detailed reference for naming structs, fields, tables, and tags in GORM entities.

## Struct Names

**PascalCase**: `Symbol`, `SymbolData`
**Singular**: Entity names are singular (table names are plural)

## Field Names

**PascalCase in Go**: `ProjectID`, `ClassName`, `ComponentTarget`
**Acronyms**: Keep uppercase: `ID`, `UID` (not `Id`, `Uid`)

## Table Names

**snake_case**: `symbols`, `symbol_data`
**Plural**: Use plural form of entity name
**Method**: Value receiver, returns string literal

Example:
```go
func (Symbol) TableName() string {
	return "symbols"
}
```

## JSON Tag Naming

**snake_case**: `project_id`, `class_name`, `component_target`
**Consistent conversion**: PascalCase → snake_case

Examples:
```go
ProjectID       uint32 `json:"project_id"`
ClassName       string `json:"class_name"`
ComponentTarget string `json:"component_target"`
```
