package identify

import (
	"database/sql"
	"fmt"
	"strings"
	"time"

	"github.com/google/uuid"
)

// PersonFact represents a piece of PII extracted about a person
type PersonFact struct {
	ID                 string
	PersonID           string
	Category           string
	FactType           string
	FactValue          string
	Confidence         float64
	SourceType         string
	SourceChannel      *string
	SourceSegment      *string
	SourceFacetID      *string
	Evidence           *string
	IsSensitive        bool
	IsIdentifier       bool
	IsHardIdentifier   bool
	CreatedAt          time.Time
	UpdatedAt          time.Time
}

// Fact type constants - Hard identifiers
const (
	FactTypeEmailPersonal      = "email_personal"
	FactTypeEmailWork          = "email_work"
	FactTypeEmailSchool        = "email_school"
	FactTypePhoneMobile        = "phone_mobile"
	FactTypePhoneHome          = "phone_home"
	FactTypePhoneWork          = "phone_work"
	FactTypeFullLegalName      = "full_legal_name"
	FactTypeSocialTwitter      = "social_twitter"
	FactTypeSocialInstagram    = "social_instagram"
	FactTypeSocialLinkedIn     = "social_linkedin"
	FactTypeSocialFacebook     = "social_facebook"
	FactTypeSocialTikTok       = "social_tiktok"
	FactTypeSocialReddit       = "social_reddit"
	FactTypeSocialDiscord      = "social_discord"
	FactTypeUsernameGeneric    = "username_generic"
	FactTypeSSN                = "ssn"
	FactTypePassportNumber     = "passport_number"
	FactTypeDriversLicense     = "drivers_license"
)

// Fact type constants - Compound/Soft identifiers
const (
	FactTypeGivenName          = "given_name"
	FactTypeFamilyName         = "family_name"
	FactTypeBirthdate          = "birthdate"
	FactTypeEmployerCurrent    = "employer_current"
	FactTypeBusinessOwned      = "business_owned"
	FactTypeBusinessRole       = "business_role"
	FactTypeLocationCurrent    = "location_current"
	FactTypeProfession         = "profession"
	FactTypeSpouseFirstName    = "spouse_first_name"
	FactTypeSchoolAttended     = "school_attended"
)

// Fact categories
const (
	CategoryCoreIdentity     = "core_identity"
	CategoryContactInfo      = "contact_information"
	CategoryProfessional     = "professional"
	CategoryRelationships    = "relationships"
	CategoryLocation         = "location_presence"
	CategoryEducation        = "education"
	CategoryGovernmentID     = "government_legal_ids"
	CategoryFinancial        = "financial"
	CategoryMedical          = "medical_health"
	CategoryLifeEvents       = "life_events_dates"
	CategoryPreferences      = "preferences_lifestyle"
	CategoryVehiclesProperty = "vehicles_property"
	CategoryDigitalIdentity  = "digital_identity"
	CategoryPhysical         = "physical_description"
)

// HardIdentifiers is a list of fact types that trigger immediate merge consideration
var HardIdentifiers = []string{
	FactTypeEmailPersonal,
	FactTypeEmailWork,
	FactTypeEmailSchool,
	FactTypePhoneMobile,
	FactTypePhoneHome,
	FactTypePhoneWork,
	FactTypeFullLegalName,
	FactTypeSocialTwitter,
	FactTypeSocialInstagram,
	FactTypeSocialLinkedIn,
	FactTypeSocialFacebook,
	FactTypeSocialTikTok,
	FactTypeSocialReddit,
	FactTypeSocialDiscord,
	FactTypeUsernameGeneric,
	FactTypeSSN,
	FactTypePassportNumber,
	FactTypeDriversLicense,
}

// Tier1Identifiers are strong identifiers for high-precision matching.
// These explicitly exclude full_legal_name to avoid label leakage.
var Tier1Identifiers = []string{
	FactTypeEmailPersonal,
	FactTypeEmailWork,
	FactTypeEmailSchool,
	FactTypePhoneMobile,
	FactTypePhoneHome,
	FactTypePhoneWork,
	FactTypeSocialTwitter,
	FactTypeSocialInstagram,
	FactTypeSocialLinkedIn,
	FactTypeSocialFacebook,
	FactTypeSocialTikTok,
	FactTypeSocialReddit,
	FactTypeSocialDiscord,
	FactTypeUsernameGeneric,
	FactTypeSSN,
	FactTypePassportNumber,
	FactTypeDriversLicense,
}

// SoftIdentifierWeights maps soft identifier types to their weight in similarity scoring
var SoftIdentifierWeights = map[string]float64{
	FactTypeEmployerCurrent: 0.20,
	FactTypeLocationCurrent: 0.15,
	FactTypeProfession:      0.15,
	FactTypeSpouseFirstName: 0.25,
	FactTypeSchoolAttended:  0.15,
	FactTypeBirthdate:       0.25,
}

// InsertFact inserts or updates a person fact
// Uses UNIQUE constraint on (person_id, category, fact_type, fact_value) to prevent duplicates
func InsertFact(db *sql.DB, fact PersonFact) error {
	if fact.ID == "" {
		fact.ID = uuid.New().String()
	}

	now := time.Now().Unix()
	if fact.CreatedAt.IsZero() {
		fact.CreatedAt = time.Unix(now, 0)
	}
	fact.UpdatedAt = time.Unix(now, 0)

	// Determine identifier flags based on fact type
	fact.IsIdentifier = isIdentifierType(fact.FactType)
	fact.IsHardIdentifier = isHardIdentifierType(fact.FactType)

	_, err := db.Exec(`
		INSERT INTO person_facts (
			id, person_id, category, fact_type, fact_value,
			confidence, source_type, source_channel, source_segment_id,
			source_facet_id, evidence, is_sensitive, is_identifier, is_hard_identifier,
			created_at, updated_at
		) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
		ON CONFLICT(person_id, category, fact_type, fact_value) DO UPDATE SET
			confidence = MAX(confidence, excluded.confidence),
			source_type = excluded.source_type,
			source_channel = COALESCE(excluded.source_channel, source_channel),
			source_segment_id = COALESCE(excluded.source_segment_id, source_segment_id),
			source_facet_id = COALESCE(excluded.source_facet_id, source_facet_id),
			evidence = COALESCE(excluded.evidence, evidence),
			updated_at = excluded.updated_at
	`,
		fact.ID, fact.PersonID, fact.Category, fact.FactType, fact.FactValue,
		fact.Confidence, fact.SourceType, fact.SourceChannel, fact.SourceSegment,
		fact.SourceFacetID, fact.Evidence, boolToInt(fact.IsSensitive),
		boolToInt(fact.IsIdentifier), boolToInt(fact.IsHardIdentifier),
		fact.CreatedAt.Unix(), fact.UpdatedAt.Unix(),
	)

	if err != nil {
		return fmt.Errorf("failed to insert fact: %w", err)
	}

	return nil
}

// GetFactsForPerson returns all facts for a person
func GetFactsForPerson(db *sql.DB, personID string) ([]PersonFact, error) {
	rows, err := db.Query(`
		SELECT
			id, person_id, category, fact_type, fact_value,
			confidence, source_type, source_channel, source_segment_id,
			source_facet_id, evidence, is_sensitive, is_identifier, is_hard_identifier,
			created_at, updated_at
		FROM person_facts
		WHERE person_id = ?
		ORDER BY category, fact_type, confidence DESC
	`, personID)
	if err != nil {
		return nil, fmt.Errorf("failed to query facts: %w", err)
	}
	defer rows.Close()

	var facts []PersonFact
	for rows.Next() {
		fact, err := scanPersonFact(rows)
		if err != nil {
			return nil, err
		}
		facts = append(facts, fact)
	}

	return facts, rows.Err()
}

// GetHardIdentifiers returns all hard identifier facts across all persons
func GetHardIdentifiers(db *sql.DB) ([]PersonFact, error) {
	rows, err := db.Query(`
		SELECT
			id, person_id, category, fact_type, fact_value,
			confidence, source_type, source_channel, source_segment_id,
			source_facet_id, evidence, is_sensitive, is_identifier, is_hard_identifier,
			created_at, updated_at
		FROM person_facts
		WHERE is_hard_identifier = 1
		ORDER BY fact_type, fact_value
	`)
	if err != nil {
		return nil, fmt.Errorf("failed to query hard identifiers: %w", err)
	}
	defer rows.Close()

	var facts []PersonFact
	for rows.Next() {
		fact, err := scanPersonFact(rows)
		if err != nil {
			return nil, err
		}
		facts = append(facts, fact)
	}

	return facts, rows.Err()
}

// GetFactsByType returns all facts of a specific type
func GetFactsByType(db *sql.DB, factType string) ([]PersonFact, error) {
	rows, err := db.Query(`
		SELECT
			id, person_id, category, fact_type, fact_value,
			confidence, source_type, source_channel, source_segment_id,
			source_facet_id, evidence, is_sensitive, is_identifier, is_hard_identifier,
			created_at, updated_at
		FROM person_facts
		WHERE fact_type = ?
		ORDER BY person_id, confidence DESC
	`, factType)
	if err != nil {
		return nil, fmt.Errorf("failed to query facts by type: %w", err)
	}
	defer rows.Close()

	var facts []PersonFact
	for rows.Next() {
		fact, err := scanPersonFact(rows)
		if err != nil {
			return nil, err
		}
		facts = append(facts, fact)
	}

	return facts, rows.Err()
}

// GetFactsByCategory returns all facts in a specific category for a person
func GetFactsByCategory(db *sql.DB, personID string, category string) ([]PersonFact, error) {
	rows, err := db.Query(`
		SELECT
			id, person_id, category, fact_type, fact_value,
			confidence, source_type, source_channel, source_segment_id,
			source_facet_id, evidence, is_sensitive, is_identifier, is_hard_identifier,
			created_at, updated_at
		FROM person_facts
		WHERE person_id = ? AND category = ?
		ORDER BY fact_type, confidence DESC
	`, personID, category)
	if err != nil {
		return nil, fmt.Errorf("failed to query facts by category: %w", err)
	}
	defer rows.Close()

	var facts []PersonFact
	for rows.Next() {
		fact, err := scanPersonFact(rows)
		if err != nil {
			return nil, err
		}
		facts = append(facts, fact)
	}

	return facts, rows.Err()
}

// FactCollision represents multiple persons sharing the same fact value
type FactCollision struct {
	FactType   string
	FactValue  string
	PersonIDs  []string
	Confidence float64 // average confidence across all instances
}

// FindFactCollisions finds instances where multiple persons share the same fact value
// This is the core of the O(F) identifier-centric resolution algorithm
func FindFactCollisions(db *sql.DB, factType string) ([]FactCollision, error) {
	rows, err := db.Query(`
		SELECT
			fact_type,
			fact_value,
			GROUP_CONCAT(person_id) as person_ids,
			AVG(confidence) as avg_confidence,
			COUNT(DISTINCT person_id) as person_count
		FROM person_facts
		WHERE fact_type = ?
		GROUP BY fact_type, fact_value
		HAVING person_count > 1
		ORDER BY person_count DESC, avg_confidence DESC
	`, factType)
	if err != nil {
		return nil, fmt.Errorf("failed to query fact collisions: %w", err)
	}
	defer rows.Close()

	var collisions []FactCollision
	for rows.Next() {
		var collision FactCollision
		var personIDsStr string
		var personCount int

		err := rows.Scan(
			&collision.FactType,
			&collision.FactValue,
			&personIDsStr,
			&collision.Confidence,
			&personCount,
		)
		if err != nil {
			return nil, fmt.Errorf("failed to scan collision: %w", err)
		}

		// Parse comma-separated person IDs
		collision.PersonIDs = splitPersonIDs(personIDsStr)

		collisions = append(collisions, collision)
	}

	return collisions, rows.Err()
}

// FindAllHardIdentifierCollisions finds all collisions across all hard identifier types
func FindAllHardIdentifierCollisions(db *sql.DB) ([]FactCollision, error) {
	rows, err := db.Query(`
		SELECT
			fact_type,
			fact_value,
			GROUP_CONCAT(person_id) as person_ids,
			AVG(confidence) as avg_confidence,
			COUNT(DISTINCT person_id) as person_count
		FROM person_facts
		WHERE is_hard_identifier = 1
		GROUP BY fact_type, fact_value
		HAVING person_count > 1
		ORDER BY person_count DESC, avg_confidence DESC
	`)
	if err != nil {
		return nil, fmt.Errorf("failed to query hard identifier collisions: %w", err)
	}
	defer rows.Close()

	var collisions []FactCollision
	for rows.Next() {
		var collision FactCollision
		var personIDsStr string
		var personCount int

		err := rows.Scan(
			&collision.FactType,
			&collision.FactValue,
			&personIDsStr,
			&collision.Confidence,
			&personCount,
		)
		if err != nil {
			return nil, fmt.Errorf("failed to scan collision: %w", err)
		}

		collision.PersonIDs = splitPersonIDs(personIDsStr)
		collisions = append(collisions, collision)
	}

	return collisions, rows.Err()
}

// FindTier1IdentifierCollisions finds collisions across Tier 1 identifiers only.
// Uses a normalized value to dedupe trivial variants before matching.
func FindTier1IdentifierCollisions(db *sql.DB) ([]FactCollision, error) {
	placeholders := strings.Repeat("?,", len(Tier1Identifiers))
	placeholders = strings.TrimSuffix(placeholders, ",")

	normalizedExpr := `
		CASE
			WHEN fact_type IN ('phone_mobile','phone_home','phone_work') THEN
				LOWER(TRIM(
					REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(fact_value, '-', ''), ' ', ''), '(', ''), ')', ''), '+', ''), '.', '')
				))
			WHEN fact_type IN ('social_twitter','social_instagram','social_linkedin','social_facebook','social_tiktok','social_reddit','social_discord','username_generic') THEN
				LOWER(TRIM(REPLACE(fact_value, '@', '')))
			ELSE
				LOWER(TRIM(fact_value))
		END
	`

	query := fmt.Sprintf(`
		SELECT
			fact_type,
			%s AS fact_value,
			GROUP_CONCAT(person_id) as person_ids,
			AVG(confidence) as avg_confidence,
			COUNT(DISTINCT person_id) as person_count
		FROM person_facts
		WHERE fact_type IN (%s)
		GROUP BY fact_type, fact_value
		HAVING person_count > 1
		ORDER BY person_count DESC, avg_confidence DESC
	`, normalizedExpr, placeholders)

	args := make([]interface{}, 0, len(Tier1Identifiers))
	for _, v := range Tier1Identifiers {
		args = append(args, v)
	}

	rows, err := db.Query(query, args...)
	if err != nil {
		return nil, fmt.Errorf("failed to query tier1 collisions: %w", err)
	}
	defer rows.Close()

	var collisions []FactCollision
	for rows.Next() {
		var collision FactCollision
		var personIDsStr string
		var personCount int
		if err := rows.Scan(
			&collision.FactType,
			&collision.FactValue,
			&personIDsStr,
			&collision.Confidence,
			&personCount,
		); err != nil {
			return nil, fmt.Errorf("failed to scan collision: %w", err)
		}
		collision.PersonIDs = splitPersonIDs(personIDsStr)
		collisions = append(collisions, collision)
	}

	return collisions, rows.Err()
}

// Helper functions

func scanPersonFact(rows *sql.Rows) (PersonFact, error) {
	var fact PersonFact
	var sourceChannel, sourceSegment, sourceFacetID, evidence sql.NullString
	var isSensitive, isIdentifier, isHardIdentifier int
	var createdAt, updatedAt int64

	err := rows.Scan(
		&fact.ID, &fact.PersonID, &fact.Category, &fact.FactType, &fact.FactValue,
		&fact.Confidence, &fact.SourceType, &sourceChannel, &sourceSegment,
		&sourceFacetID, &evidence, &isSensitive, &isIdentifier, &isHardIdentifier,
		&createdAt, &updatedAt,
	)
	if err != nil {
		return fact, fmt.Errorf("failed to scan fact: %w", err)
	}

	if sourceChannel.Valid {
		fact.SourceChannel = &sourceChannel.String
	}
	if sourceSegment.Valid {
		fact.SourceSegment = &sourceSegment.String
	}
	if sourceFacetID.Valid {
		fact.SourceFacetID = &sourceFacetID.String
	}
	if evidence.Valid {
		fact.Evidence = &evidence.String
	}

	fact.IsSensitive = isSensitive == 1
	fact.IsIdentifier = isIdentifier == 1
	fact.IsHardIdentifier = isHardIdentifier == 1
	fact.CreatedAt = time.Unix(createdAt, 0)
	fact.UpdatedAt = time.Unix(updatedAt, 0)

	return fact, nil
}

func isIdentifierType(factType string) bool {
	// Hard identifiers are always identifiers
	if isHardIdentifierType(factType) {
		return true
	}

	// Soft identifiers used in matching
	_, isSoft := SoftIdentifierWeights[factType]
	return isSoft
}

func isHardIdentifierType(factType string) bool {
	for _, hard := range HardIdentifiers {
		if factType == hard {
			return true
		}
	}
	return false
}

func boolToInt(b bool) int {
	if b {
		return 1
	}
	return 0
}

func splitPersonIDs(personIDsStr string) []string {
	if personIDsStr == "" {
		return nil
	}
	// SQLite GROUP_CONCAT uses comma separator by default
	// Note: This assumes person IDs don't contain commas
	personIDs := []string{}
	start := 0
	for i := 0; i < len(personIDsStr); i++ {
		if personIDsStr[i] == ',' {
			personIDs = append(personIDs, personIDsStr[start:i])
			start = i + 1
		}
	}
	if start < len(personIDsStr) {
		personIDs = append(personIDs, personIDsStr[start:])
	}
	return personIDs
}
