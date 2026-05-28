package memory

import "strings"

// EntityType represents a type of entity in the knowledge graph.
// Entity types are code-defined (not stored in database) to enable
// type-specific resolution strategies while keeping the schema simple.
type EntityType struct {
	ID          int    // Numeric identifier stored in entities.entity_type_id
	Name        string // Display name (e.g., "Person", "Company")
	Description string // Human-readable description
}

// DefaultEntityTypes defines the standard entity types for the memory system.
// These map to entities.entity_type_id in the database.
//
// Philosophy: Entities are things you want to traverse to/from.
// Abstract concepts (hobbies, professions) are discoverable via embedding search.
// Literal values (emails, phones, dates) use target_literal on relationships.
var DefaultEntityTypes = []EntityType{
	{ID: 0, Name: "Entity", Description: "Default/unknown type"},
	{ID: 1, Name: "Person", Description: "A human being"},
	{ID: 2, Name: "Organization", Description: "Company, institution, government, court, school, or group"},
	{ID: 3, Name: "Project", Description: "A project, product, or codebase"},
	{ID: 4, Name: "Location", Description: "A place (city, address, venue)"},
	{ID: 5, Name: "Event", Description: "A meeting, occurrence, or happening"},
	{ID: 6, Name: "Document", Description: "A file, article, or written work"},
	{ID: 7, Name: "Pet", Description: "An animal companion"},
}

// Entity type ID constants for convenience
const (
	EntityTypeEntity       = 0 // Default/unknown type
	EntityTypePerson       = 1 // A human being
	EntityTypeOrganization = 2 // Company, institution, government, court, school
	EntityTypeProject      = 3 // A project, product, or codebase
	EntityTypeLocation     = 4 // A place (city, address, venue)
	EntityTypeEvent        = 5 // A meeting, occurrence, or happening
	EntityTypeDocument     = 6 // A file, article, or written work
	EntityTypePet          = 7 // An animal companion
)

// GetEntityTypeByID returns the EntityType for the given ID, or nil if not found.
func GetEntityTypeByID(id int) *EntityType {
	for i := range DefaultEntityTypes {
		if DefaultEntityTypes[i].ID == id {
			return &DefaultEntityTypes[i]
		}
	}
	return nil
}

// GetEntityTypeByName returns the EntityType for the given name (case-insensitive),
// or nil if not found.
func GetEntityTypeByName(name string) *EntityType {
	nameLower := strings.ToLower(name)
	for i := range DefaultEntityTypes {
		if strings.ToLower(DefaultEntityTypes[i].Name) == nameLower {
			return &DefaultEntityTypes[i]
		}
	}
	return nil
}

// IsValidEntityTypeID returns true if the given ID is a valid entity type ID.
func IsValidEntityTypeID(id int) bool {
	return GetEntityTypeByID(id) != nil
}

// EntityTypeNames returns a slice of all entity type names.
func EntityTypeNames() []string {
	names := make([]string, len(DefaultEntityTypes))
	for i, et := range DefaultEntityTypes {
		names[i] = et.Name
	}
	return names
}
