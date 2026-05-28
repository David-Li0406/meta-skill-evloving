package identify

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"strings"
	"time"

	"github.com/google/uuid"
)

// FacetToFactMapping maps facet types from PII extraction to person_facts fields
var FacetToFactMapping = map[string]struct {
	Category string
	FactType string
}{
	"pii_email_personal":    {CategoryContactInfo, FactTypeEmailPersonal},
	"pii_email_work":        {CategoryContactInfo, FactTypeEmailWork},
	"pii_email_school":      {CategoryContactInfo, FactTypeEmailSchool},
	"pii_phone_mobile":      {CategoryContactInfo, FactTypePhoneMobile},
	"pii_phone_home":        {CategoryContactInfo, FactTypePhoneHome},
	"pii_phone_work":        {CategoryContactInfo, FactTypePhoneWork},
	"pii_full_legal_name":   {CategoryCoreIdentity, FactTypeFullLegalName},
	"pii_given_name":        {CategoryCoreIdentity, FactTypeGivenName},
	"pii_family_name":       {CategoryCoreIdentity, FactTypeFamilyName},
	"pii_birthdate":         {CategoryCoreIdentity, FactTypeBirthdate},
	"pii_employer_current":  {CategoryProfessional, FactTypeEmployerCurrent},
	"pii_business_owned":    {CategoryProfessional, FactTypeBusinessOwned},
	"pii_business_role":     {CategoryProfessional, FactTypeBusinessRole},
	"pii_profession":        {CategoryProfessional, FactTypeProfession},
	"pii_location_current":  {CategoryLocation, FactTypeLocationCurrent},
	"pii_spouse_first_name": {CategoryRelationships, FactTypeSpouseFirstName},
	"pii_school_attended":   {CategoryEducation, FactTypeSchoolAttended},
	"pii_social_twitter":    {CategoryDigitalIdentity, FactTypeSocialTwitter},
	"pii_social_instagram":  {CategoryDigitalIdentity, FactTypeSocialInstagram},
	"pii_social_linkedin":   {CategoryDigitalIdentity, FactTypeSocialLinkedIn},
	"pii_social_facebook":   {CategoryDigitalIdentity, FactTypeSocialFacebook},
	"pii_username_generic":  {CategoryDigitalIdentity, FactTypeUsernameGeneric},
	"pii_ssn":               {CategoryGovernmentID, FactTypeSSN},
	"pii_passport_number":   {CategoryGovernmentID, FactTypePassportNumber},
	"pii_drivers_license":   {CategoryGovernmentID, FactTypeDriversLicense},
}

// SyncStats holds statistics about a sync operation
type SyncStats struct {
	AnalysisRunsProcessed int
	FacetsProcessed       int
	FactsCreated          int
	FactsUpdated          int
	UnattributedCreated   int
	ThirdPartiesCreated   int
	Errors                int
}

// SyncFacetsToPersonFacts processes facets from pii_extraction analysis runs
// and creates/updates person_facts entries
func SyncFacetsToPersonFacts(db *sql.DB) (*SyncStats, error) {
	stats := &SyncStats{}

	// Get completed pii_extraction analysis runs with JSON output
	rows, err := db.Query(`
		SELECT DISTINCT ar.id, ar.segment_id
		FROM analysis_runs ar
		JOIN analysis_types at ON ar.analysis_type_id = at.id
		WHERE at.name = 'pii_extraction'
		AND ar.status = 'completed'
		AND ar.output_text IS NOT NULL
		AND ar.output_text != ''
	`)
	if err != nil {
		return nil, fmt.Errorf("query analysis runs: %w", err)
	}

	var runs []struct {
		ID        string
		SegmentID string
	}
	for rows.Next() {
		var run struct {
			ID        string
			SegmentID string
		}
		if err := rows.Scan(&run.ID, &run.SegmentID); err != nil {
			rows.Close()
			return nil, err
		}
		runs = append(runs, run)
	}
	rows.Close()
	if err := rows.Err(); err != nil {
		return nil, err
	}

	for _, run := range runs {
		runStats, err := syncAnalysisRun(db, run.ID, run.SegmentID)
		if err != nil {
			stats.Errors++
			continue
		}
		stats.AnalysisRunsProcessed++
		stats.FacetsProcessed += runStats.FacetsProcessed
		stats.FactsCreated += runStats.FactsCreated
		stats.FactsUpdated += runStats.FactsUpdated
		stats.UnattributedCreated += runStats.UnattributedCreated
		stats.ThirdPartiesCreated += runStats.ThirdPartiesCreated
	}

	return stats, nil
}

// syncAnalysisRun processes a single analysis run's facets
func syncAnalysisRun(db *sql.DB, runID, segmentID string) (*SyncStats, error) {
	stats := &SyncStats{}

	// Get the channel for this segment (for source_channel)
	var channel sql.NullString
	err := db.QueryRow(`
		SELECT channel FROM segments WHERE id = ?
	`, segmentID).Scan(&channel)
	if err != nil {
		return nil, fmt.Errorf("get segment channel: %w", err)
	}

	// Prefer parsing full JSON output for attribution-aware facts.
	var outputText sql.NullString
	if err := db.QueryRow(`SELECT output_text FROM analysis_runs WHERE id = ?`, runID).Scan(&outputText); err == nil {
		if outputText.Valid && outputText.String != "" {
			runStats, err := ProcessPIIExtractionOutput(db, runID, segmentID, outputText.String)
			if err == nil {
				// Use JSON output path only to avoid duplicate unattributed facts.
				return runStats, nil
			}
		}
	}

	// Get all facets for this analysis run
	rows, err := db.Query(`
		SELECT id, facet_type, value, person_id, confidence, metadata_json
		FROM facets
		WHERE analysis_run_id = ?
	`, runID)
	if err != nil {
		return nil, fmt.Errorf("query facets: %w", err)
	}

	type facetRow struct {
		FacetID      string
		FacetType    string
		Value        string
		PersonID     sql.NullString
		Confidence   sql.NullFloat64
		MetadataJSON sql.NullString
	}

	var facets []facetRow
	for rows.Next() {
		var f facetRow
		if err := rows.Scan(&f.FacetID, &f.FacetType, &f.Value, &f.PersonID, &f.Confidence, &f.MetadataJSON); err != nil {
			stats.Errors++
			continue
		}
		facets = append(facets, f)
	}
	rows.Close()
	if err := rows.Err(); err != nil {
		return nil, err
	}

	now := time.Now().Unix()

	for _, f := range facets {
		facetID := f.FacetID
		facetType := f.FacetType
		value := f.Value
		personID := f.PersonID
		confidence := f.Confidence
		metadataJSON := f.MetadataJSON

		stats.FacetsProcessed++

		// Skip empty values
		if value == "" {
			continue
		}

		// Map facet type to fact type
		mapping, ok := FacetToFactMapping[facetType]
		if !ok {
			continue // Unknown facet type, skip
		}

		// Extract source type and evidence from metadata
		sourceType := "extracted"
		var evidence *string
		if metadataJSON.Valid {
			var meta map[string]interface{}
			if json.Unmarshal([]byte(metadataJSON.String), &meta) == nil {
				if st, ok := meta["source_type"].(string); ok {
					sourceType = st
				}
				if ev, ok := meta["evidence"].(string); ok {
					evidence = &ev
				}
			}
		}

		// If no person_id, this is an unattributed fact
		if !personID.Valid || personID.String == "" {
			// Insert into unattributed_facts
			_, err := db.Exec(`
				INSERT INTO unattributed_facts (
					id, fact_type, fact_value, source_segment_id, context, created_at
				) VALUES (?, ?, ?, ?, ?, ?)
				ON CONFLICT DO NOTHING
			`, uuid.New().String(), mapping.FactType, value, segmentID, metadataJSON.String, now)
			if err == nil {
				stats.UnattributedCreated++
			}
			continue
		}

		// Create person fact
		fact := PersonFact{
			PersonID:           personID.String,
			Category:           mapping.Category,
			FactType:           mapping.FactType,
			FactValue:          value,
			Confidence:         0.5,
			SourceType:         sourceType,
			SourceSegment:      &segmentID,
			SourceFacetID:      &facetID,
			Evidence:           evidence,
		}

		if confidence.Valid {
			fact.Confidence = confidence.Float64
		}
		if channel.Valid {
			fact.SourceChannel = &channel.String
		}

		// Determine if sensitive
		fact.IsSensitive = isSensitiveFactType(mapping.FactType)

		err := InsertFact(db, fact)
		if err != nil {
			stats.Errors++
		} else {
			stats.FactsCreated++
		}
	}

	return stats, rows.Err()
}

// SyncSingleRun processes a single analysis run by ID
func SyncSingleRun(db *sql.DB, runID string) (*SyncStats, error) {
	var segmentID string
	err := db.QueryRow(`SELECT segment_id FROM analysis_runs WHERE id = ?`, runID).Scan(&segmentID)
	if err != nil {
		return nil, fmt.Errorf("get analysis run: %w", err)
	}
	return syncAnalysisRun(db, runID, segmentID)
}

// isSensitiveFactType determines if a fact type should be marked as sensitive
func isSensitiveFactType(factType string) bool {
	sensitiveTypes := map[string]bool{
		FactTypeSSN:            true,
		FactTypePassportNumber: true,
		FactTypeDriversLicense: true,
	}
	return sensitiveTypes[factType]
}

// ProcessPIIExtractionOutput processes the full JSON output from PII extraction
// This is called after the LLM returns structured output to sync ALL extracted data
func ProcessPIIExtractionOutput(db *sql.DB, runID, segmentID, outputJSON string) (*SyncStats, error) {
	stats := &SyncStats{}

	type factShape struct {
		SubjectKind      string `json:"subject_kind"`
		SubjectRef       string `json:"subject_ref"`
		Category         string `json:"category"`
		FactType         string `json:"fact_type"`
		Value            string `json:"value"`
		Confidence       string `json:"confidence"`
		Evidence         string `json:"evidence"`
		SelfDisclosed    bool   `json:"self_disclosed"`
		Source           string `json:"source"`
		RelatedPersonRef string `json:"related_person_ref"`
		Note             string `json:"note"`
	}

	type outputShape struct {
		ExtractionMetadata struct {
			Channel                  string `json:"channel"`
			PrimaryContactName       string `json:"primary_contact_name"`
			PrimaryContactIdentifier string `json:"primary_contact_identifier"`
		} `json:"extraction_metadata"`
		Facts             []factShape `json:"facts"`
		UnattributedFacts []struct {
			FactType             string   `json:"fact_type"`
			FactValue            string   `json:"fact_value"`
			SharedBy             string   `json:"shared_by"`
			Context              string   `json:"context"`
			PossibleAttributions []string `json:"possible_attributions"`
			Note                 string   `json:"note"`
		} `json:"unattributed_facts"`
	}

	var outputs []outputShape
	if err := json.Unmarshal([]byte(outputJSON), &outputs); err != nil {
		var single outputShape
		if err := json.Unmarshal([]byte(outputJSON), &single); err != nil {
			return nil, fmt.Errorf("parse output JSON: %w", err)
		}
		outputs = []outputShape{single}
	}

	now := time.Now().Unix()
	participants, _ := loadSegmentParticipants(db, segmentID)
	meID, _ := getMePersonID(db)

	for _, output := range outputs {
		channel := output.ExtractionMetadata.Channel
		if channel == "" {
			channel = getSegmentChannel(db, segmentID)
		}

		primaryRef := output.ExtractionMetadata.PrimaryContactName

		primaryPersonID := ""
		if output.ExtractionMetadata.PrimaryContactIdentifier != "" {
			err := db.QueryRow(`
				SELECT p.id FROM persons p
				JOIN identities i ON p.id = i.person_id
				WHERE i.identifier = ?
				LIMIT 1
			`, output.ExtractionMetadata.PrimaryContactIdentifier).Scan(&primaryPersonID)
			if err != nil {
				primaryPersonID = ""
			}
		}
		if primaryPersonID == "" {
			if matchID, ok := matchParticipantByName(participants, primaryRef); ok {
				primaryPersonID = matchID
			} else if id := singleNonMeParticipant(participants); id != "" {
				primaryPersonID = id
			}
		}

		thirdPartyFacts := map[string][]factShape{}

		for _, fact := range output.Facts {
			if fact.Category == "" || fact.FactType == "" || fact.Value == "" {
				continue
			}

			factMap := map[string]interface{}{
				"confidence":     fact.Confidence,
				"evidence":       []interface{}{fact.Evidence},
				"self_disclosed": fact.SelfDisclosed,
				"source":         fact.Source,
			}

			switch strings.ToLower(strings.TrimSpace(fact.SubjectKind)) {
			case "user":
				if meID != "" {
					processExtractedFact(db, stats, meID, fact.Category, fact.FactType, fact.Value, factMap, segmentID, channel, runID, now)
				}
			case "primary_contact":
				if primaryPersonID != "" {
					processExtractedFact(db, stats, primaryPersonID, fact.Category, fact.FactType, fact.Value, factMap, segmentID, channel, runID, now)
				}
			case "third_party":
				ref := strings.TrimSpace(fact.SubjectRef)
				if ref == "" {
					ref = "Unknown"
				}
				thirdPartyFacts[ref] = append(thirdPartyFacts[ref], fact)
			default:
				ref := strings.TrimSpace(fact.SubjectRef)
				if ref != "" {
					if matchID, ok := matchParticipantByName(participants, ref); ok {
						processExtractedFact(db, stats, matchID, fact.Category, fact.FactType, fact.Value, factMap, segmentID, channel, runID, now)
						continue
					}
				}
				ref = "Unknown"
				thirdPartyFacts[ref] = append(thirdPartyFacts[ref], fact)
			}
		}

		for ref, facts := range thirdPartyFacts {
			name := ref
			cleanFacts := map[string]string{}
			hasStrongIdentifier := false

			for _, fact := range facts {
				if fact.FactType == "" || fact.Value == "" {
					continue
				}

				mapped := mapFactKey(fact.FactType)
				if isStrongThirdPartyIdentifier(mapped) {
					hasStrongIdentifier = true
				}
				if isAllowedThirdPartyFactType(mapped) {
					if existing, ok := cleanFacts[mapped]; ok && existing != "" {
						cleanFacts[mapped] = existing + "; " + fact.Value
					} else {
						cleanFacts[mapped] = fact.Value
					}
					if mapped == FactTypeGivenName && name == "" {
						name = fact.Value
					}
				}
			}

			if !hasStrongIdentifier {
				_ = insertCandidateMention(db, name, cleanFacts, segmentID, now)
				continue
			}

			personID := uuid.New().String()
			_, err := db.Exec(`
				INSERT INTO persons (id, canonical_name, relationship_type, created_at, updated_at)
				VALUES (?, ?, 'third_party', ?, ?)
			`, personID, name, now, now)
			if err == nil {
				stats.ThirdPartiesCreated++

				for factKey, factValue := range cleanFacts {
					fact := PersonFact{
						PersonID:      personID,
						Category:      CategoryCoreIdentity,
						FactType:      factKey,
						FactValue:     factValue,
						Confidence:    0.5,
						SourceType:    "mentioned",
						SourceSegment: &segmentID,
					}
					if channel != "" {
						fact.SourceChannel = &channel
					}
					InsertFact(db, fact)
				}
			}
		}

		// Process unattributed facts
		for _, uf := range output.UnattributedFacts {
			if uf.FactValue == "" {
				continue
			}

			var sharedByPersonID sql.NullString
			if uf.SharedBy != "" {
				db.QueryRow(`
					SELECT id FROM persons 
					WHERE canonical_name LIKE ? OR display_name LIKE ?
					LIMIT 1
				`, "%"+uf.SharedBy+"%", "%"+uf.SharedBy+"%").Scan(&sharedByPersonID)
			}

			attributionsJSON, _ := json.Marshal(uf.PossibleAttributions)

			_, err := db.Exec(`
				INSERT INTO unattributed_facts (
					id, fact_type, fact_value, shared_by_person_id,
					source_segment_id, context, possible_attributions, created_at
				) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
				ON CONFLICT DO NOTHING
			`, uuid.New().String(), uf.FactType, uf.FactValue, sharedByPersonID,
				segmentID, uf.Context, string(attributionsJSON), now)
			if err == nil {
				stats.UnattributedCreated++
			}
		}
	}

	return stats, nil
}

type segmentParticipant struct {
	ID            string
	CanonicalName string
	DisplayName   string
	IsMe          bool
}

func loadSegmentParticipants(db *sql.DB, segmentID string) ([]segmentParticipant, error) {
	rows, err := db.Query(`
		SELECT DISTINCT p.id, COALESCE(p.canonical_name, ''), COALESCE(p.display_name, ''), p.is_me
		FROM persons p
		JOIN event_participants ep ON p.id = ep.person_id
		JOIN segment_events se ON se.event_id = ep.event_id
		WHERE se.segment_id = ?
	`, segmentID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var out []segmentParticipant
	for rows.Next() {
		var p segmentParticipant
		var isMe int
		if err := rows.Scan(&p.ID, &p.CanonicalName, &p.DisplayName, &isMe); err != nil {
			return nil, err
		}
		p.IsMe = isMe == 1
		out = append(out, p)
	}
	return out, rows.Err()
}

func getSegmentChannel(db *sql.DB, segmentID string) string {
	var channel sql.NullString
	_ = db.QueryRow(`SELECT channel FROM segments WHERE id = ?`, segmentID).Scan(&channel)
	if channel.Valid {
		return channel.String
	}
	return ""
}

func getMePersonID(db *sql.DB) (string, error) {
	var id string
	err := db.QueryRow(`SELECT id FROM persons WHERE is_me = 1 LIMIT 1`).Scan(&id)
	if err != nil {
		return "", err
	}
	return id, nil
}

func matchParticipantByName(participants []segmentParticipant, reference string) (string, bool) {
	ref := strings.ToLower(strings.TrimSpace(reference))
	if ref == "" {
		return "", false
	}
	for _, p := range participants {
		if strings.Contains(strings.ToLower(p.CanonicalName), ref) ||
			strings.Contains(strings.ToLower(p.DisplayName), ref) {
			return p.ID, true
		}
	}
	return "", false
}

func singleNonMeParticipant(participants []segmentParticipant) string {
	var nonMe string
	for _, p := range participants {
		if p.IsMe {
			continue
		}
		if nonMe != "" && nonMe != p.ID {
			return ""
		}
		nonMe = p.ID
	}
	return nonMe
}

func refMatchesPerson(reference, personID string, participants []segmentParticipant) bool {
	ref := strings.ToLower(strings.TrimSpace(reference))
	if ref == "" {
		return false
	}
	for _, p := range participants {
		if p.ID != personID {
			continue
		}
		if strings.Contains(strings.ToLower(p.CanonicalName), ref) ||
			strings.Contains(strings.ToLower(p.DisplayName), ref) {
			return true
		}
	}
	return false
}

// processExtractedFact handles inserting a single extracted fact
func processExtractedFact(db *sql.DB, stats *SyncStats, personID, category, factKey, value string, factMap map[string]interface{}, segmentID, channel, runID string, now int64) {
	// Map the fact key to our standard fact types
	factType := mapFactKey(factKey)
	mappedCategory := mapCategory(category)

	confidence := 0.5
	if confStr, ok := factMap["confidence"].(string); ok {
		switch confStr {
		case "high":
			confidence = 0.9
		case "medium":
			confidence = 0.7
		case "low":
			confidence = 0.4
		}
	}

	sourceType := "mentioned"
	if selfDisclosed, ok := factMap["self_disclosed"].(bool); ok && selfDisclosed {
		sourceType = "self_disclosed"
	}
	if source, ok := factMap["source"].(string); ok {
		sourceType = source
	}

	var evidence *string
	if evidenceArr, ok := factMap["evidence"].([]interface{}); ok && len(evidenceArr) > 0 {
		combined := ""
		for i, e := range evidenceArr {
			if s, ok := e.(string); ok {
				if i > 0 {
					combined += "; "
				}
				combined += s
			}
		}
		if combined != "" {
			evidence = &combined
		}
	}

	fact := PersonFact{
		PersonID:           personID,
		Category:           mappedCategory,
		FactType:           factType,
		FactValue:          value,
		Confidence:         confidence,
		SourceType:         sourceType,
		SourceSegment:      &segmentID,
		Evidence:           evidence,
		IsSensitive:        isSensitiveFactType(factType),
	}
	if channel != "" {
		fact.SourceChannel = &channel
	}

	err := InsertFact(db, fact)
	if err == nil {
		stats.FactsCreated++
	}
}

// mapFactKey maps extraction output keys to our standard fact type constants
func mapFactKey(key string) string {
	keyMap := map[string]string{
		"full_legal_name":  FactTypeFullLegalName,
		"given_name":       FactTypeGivenName,
		"family_name":      FactTypeFamilyName,
		"date_of_birth":    FactTypeBirthdate,
		"nicknames":        "nickname",
		"email_personal":   FactTypeEmailPersonal,
		"email_work":       FactTypeEmailWork,
		"email_school":     FactTypeEmailSchool,
		"phone_mobile":     FactTypePhoneMobile,
		"phone_home":       FactTypePhoneHome,
		"phone_work":       FactTypePhoneWork,
		"employer_current": FactTypeEmployerCurrent,
		"business_owned":   FactTypeBusinessOwned,
		"business_role":    FactTypeBusinessRole,
		"profession":       FactTypeProfession,
		"location_current": FactTypeLocationCurrent,
		"spouse":           FactTypeSpouseFirstName,
		"school_previous":  FactTypeSchoolAttended,
		"social_twitter":   FactTypeSocialTwitter,
		"social_instagram": FactTypeSocialInstagram,
		"social_linkedin":  FactTypeSocialLinkedIn,
		"social_facebook":  FactTypeSocialFacebook,
		"username_unknown": FactTypeUsernameGeneric,
		"ssn":              FactTypeSSN,
		"passport_number":  FactTypePassportNumber,
		"drivers_license":  FactTypeDriversLicense,
	}
	if mapped, ok := keyMap[key]; ok {
		return mapped
	}
	return key
}

// mapCategory maps extraction output categories to our standard category constants
func mapCategory(category string) string {
	catMap := map[string]string{
		"core_identity":        CategoryCoreIdentity,
		"contact_information":  CategoryContactInfo,
		"professional":         CategoryProfessional,
		"relationships":        CategoryRelationships,
		"location_presence":    CategoryLocation,
		"education":            CategoryEducation,
		"government_legal_ids": CategoryGovernmentID,
		"financial":            CategoryFinancial,
		"medical_health":       CategoryMedical,
		"digital_identity":     CategoryDigitalIdentity,
	}
	if mapped, ok := catMap[category]; ok {
		return mapped
	}
	return category
}

func isMetaKnownFactKey(key string) bool {
	k := strings.ToLower(strings.TrimSpace(key))
	if k == "" {
		return true
	}
	switch k {
	case "evidence", "context", "confidence", "note", "description":
		return true
	}
	if strings.HasPrefix(k, "relationship_to_") {
		return true
	}
	return false
}

func isStrongThirdPartyIdentifier(factType string) bool {
	switch factType {
	case FactTypeEmailPersonal, FactTypeEmailWork, FactTypeEmailSchool,
		FactTypePhoneMobile, FactTypePhoneHome, FactTypePhoneWork,
		FactTypeSocialTwitter, FactTypeSocialInstagram, FactTypeSocialLinkedIn,
		FactTypeSocialFacebook, FactTypeSocialTikTok, FactTypeSocialReddit,
		FactTypeSocialDiscord, FactTypeUsernameGeneric,
		FactTypeSSN, FactTypePassportNumber, FactTypeDriversLicense:
		return true
	}
	return false
}

func isAllowedThirdPartyFactType(factType string) bool {
	if isStrongThirdPartyIdentifier(factType) {
		return true
	}
	switch factType {
	case FactTypeFullLegalName, FactTypeGivenName, FactTypeFamilyName, "nickname":
		return true
	}
	return false
}

func insertCandidateMention(db *sql.DB, reference string, knownFacts map[string]string, segmentID string, now int64) error {
	if err := ensureCandidateMentionsTable(db); err != nil {
		return err
	}
	factsJSON, _ := json.Marshal(knownFacts)
	_, err := db.Exec(`
		INSERT INTO candidate_mentions (
			id, reference, known_facts_json, source_segment_id, created_at
		) VALUES (?, ?, ?, ?, ?)
	`, uuid.New().String(), reference, string(factsJSON), segmentID, now)
	return err
}

func ensureCandidateMentionsTable(db *sql.DB) error {
	_, err := db.Exec(`
		CREATE TABLE IF NOT EXISTS candidate_mentions (
			id TEXT PRIMARY KEY,
			reference TEXT NOT NULL,
			known_facts_json TEXT,
			source_segment_id TEXT,
			created_at INTEGER NOT NULL
		)
	`)
	return err
}
