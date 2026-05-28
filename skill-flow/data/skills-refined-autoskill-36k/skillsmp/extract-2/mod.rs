//! Extraction Skill
//!
//! Extracts structured information from unstructured text.
//! This is the first built-in skill in agent.rs.
//!
//! Supports extracting:
//! - Email addresses
//! - URLs
//! - Dates
//! - Named entities (people, organizations, locations)

use serde::{Deserialize, Serialize};
use serde_json::Value;

/// Supported extraction targets
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum ExtractionTarget {
    Email,
    Url,
    Date,
    Entity,
}

impl ExtractionTarget {
    /// Parse a target from string
    pub fn from_str(s: &str) -> Option<Self> {
        match s.to_lowercase().as_str() {
            "email" => Some(Self::Email),
            "url" => Some(Self::Url),
            "date" => Some(Self::Date),
            "entity" => Some(Self::Entity),
            _ => None,
        }
    }

    /// Get the target name as string
    pub fn as_str(&self) -> &'static str {
        match self {
            Self::Email => "email",
            Self::Url => "url",
            Self::Date => "date",
            Self::Entity => "entity",
        }
    }
}

/// Input for the extraction skill
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExtractionInput {
    /// The unstructured text to extract from
    pub text: String,
    /// What to extract from the text
    pub target: String,
}

impl ExtractionInput {
    /// Create a new extraction input
    pub fn new(text: impl Into<String>, target: impl Into<String>) -> Self {
        Self {
            text: text.into(),
            target: target.into(),
        }
    }

    /// Validate the input
    pub fn validate(&self) -> Result<ExtractionTarget, SkillError> {
        // Check for empty text
        if self.text.is_empty() {
            return Err(SkillError::EmptyInput);
        }

        // Validate target
        ExtractionTarget::from_str(&self.target)
            .ok_or_else(|| SkillError::InvalidTarget(self.target.clone()))
    }
}

/// Output from the extraction skill
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExtractionOutput {
    /// The extraction result as JSON
    /// Structure depends on target type
    #[serde(flatten)]
    pub result: Value,
}

impl ExtractionOutput {
    /// Create output for email extraction
    pub fn emails(emails: Vec<String>) -> Self {
        Self {
            result: serde_json::json!({ "email": emails }),
        }
    }

    /// Create output for URL extraction
    pub fn urls(urls: Vec<String>) -> Self {
        Self {
            result: serde_json::json!({ "url": urls }),
        }
    }

    /// Create output for date extraction
    pub fn dates(dates: Vec<String>) -> Self {
        Self {
            result: serde_json::json!({ "date": dates }),
        }
    }

    /// Create output for entity extraction
    pub fn entities(people: Vec<String>, orgs: Vec<String>, locations: Vec<String>) -> Self {
        Self {
            result: serde_json::json!({
                "entity": {
                    "people": people,
                    "organizations": orgs,
                    "locations": locations
                }
            }),
        }
    }

    /// Check if the output contains the expected target field
    pub fn has_target_field(&self, target: ExtractionTarget) -> bool {
        self.result.get(target.as_str()).is_some()
    }

    /// Get the output as JSON string
    pub fn to_json(&self) -> String {
        serde_json::to_string(&self.result).unwrap_or_default()
    }

    /// Parse from JSON value
    pub fn from_json(value: Value) -> Result<Self, SkillError> {
        Ok(Self { result: value })
    }
}

/// Errors that can occur during skill execution
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum SkillError {
    /// The input text is empty
    EmptyInput,
    /// The specified target is not supported
    InvalidTarget(String),
    /// The skill output is not valid JSON
    MalformedOutput(String),
    /// The output does not match the expected schema
    SchemaViolation(String),
    /// Extracted value not found in source text (hallucination)
    HallucinationDetected(String),
}

impl std::fmt::Display for SkillError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::EmptyInput => write!(f, "EmptyInput: the input text is empty"),
            Self::InvalidTarget(t) => write!(f, "InvalidTarget: unknown target '{}'", t),
            Self::MalformedOutput(msg) => write!(f, "MalformedOutput: {}", msg),
            Self::SchemaViolation(msg) => write!(f, "SchemaViolation: {}", msg),
            Self::HallucinationDetected(val) => {
                write!(f, "HallucinationDetected: '{}' not found in source text", val)
            }
        }
    }
}

/// Result type for skill operations
pub type SkillResult<T> = Result<T, SkillError>;

/// Skill request parsed from model output
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SkillRequest {
    /// The skill name (e.g., "extract")
    pub skill: String,
    /// The skill parameters
    #[serde(flatten)]
    pub params: Value,
}

impl SkillRequest {
    /// Create a new skill request
    pub fn new(skill: impl Into<String>, params: Value) -> Self {
        Self {
            skill: skill.into(),
            params,
        }
    }

    /// Check if this is an extraction skill request
    pub fn is_extraction(&self) -> bool {
        self.skill == "extract"
    }

    /// Parse extraction input from params
    pub fn parse_extraction_input(&self) -> SkillResult<ExtractionInput> {
        let text = self.params.get("text")
            .and_then(|v| v.as_str())
            .ok_or_else(|| SkillError::SchemaViolation("missing 'text' field".to_string()))?;

        let target = self.params.get("target")
            .and_then(|v| v.as_str())
            .ok_or_else(|| SkillError::SchemaViolation("missing 'target' field".to_string()))?;

        Ok(ExtractionInput::new(text, target))
    }
}

/// Result of skill execution
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SkillResponse {
    /// Whether the skill executed successfully
    pub success: bool,
    /// The skill output (if successful)
    pub output: Option<Value>,
    /// Error information (if failed)
    pub error: Option<String>,
}

impl SkillResponse {
    /// Create a successful response
    pub fn success(output: ExtractionOutput) -> Self {
        Self {
            success: true,
            output: Some(output.result),
            error: None,
        }
    }

    /// Create a failure response
    pub fn failure(error: SkillError) -> Self {
        Self {
            success: false,
            output: None,
            error: Some(error.to_string()),
        }
    }

    /// Get the output as JSON string
    pub fn to_json(&self) -> String {
        if let Some(ref output) = self.output {
            serde_json::to_string(output).unwrap_or_default()
        } else if let Some(ref error) = self.error {
            serde_json::json!({ "error": error }).to_string()
        } else {
            "{}".to_string()
        }
    }
}

/// Skill metadata for registration
#[derive(Debug, Clone)]
pub struct SkillMetadata {
    pub name: &'static str,
    pub description: &'static str,
    pub version: &'static str,
}

/// Extraction skill metadata
pub const EXTRACTION_SKILL: SkillMetadata = SkillMetadata {
    name: "extract",
    description: "Extract structured information from unstructured text",
    version: "1.0.0",
};

/// Validate extraction output against input (guardrail)
///
/// This is the core guardrail for the extraction skill.
/// It ensures:
/// 1. Output is valid JSON
/// 2. Output contains the expected target field
/// 3. Extracted values appear in the source text (no hallucination)
pub fn validate_extraction_output(
    input: &ExtractionInput,
    output: &ExtractionOutput,
    target: ExtractionTarget,
) -> SkillResult<()> {
    // Check target field exists
    if !output.has_target_field(target) {
        return Err(SkillError::SchemaViolation(format!(
            "output missing '{}' field",
            target.as_str()
        )));
    }

    // Validate extracted values appear in source text (anti-hallucination)
    let source_lower = input.text.to_lowercase();

    match target {
        ExtractionTarget::Email | ExtractionTarget::Url | ExtractionTarget::Date => {
            if let Some(values) = output.result.get(target.as_str()) {
                let items: Vec<&str> = match values {
                    Value::String(s) => vec![s.as_str()],
                    Value::Array(arr) => arr.iter()
                        .filter_map(|v| v.as_str())
                        .collect(),
                    _ => vec![],
                };

                for item in items {
                    // Check if the extracted value appears in source
                    // (case-insensitive for robustness)
                    if !source_lower.contains(&item.to_lowercase()) {
                        return Err(SkillError::HallucinationDetected(item.to_string()));
                    }
                }
            }
        }
        ExtractionTarget::Entity => {
            // For entities, check each extracted name/org/location
            if let Some(entity) = output.result.get("entity") {
                for field in ["people", "organizations", "locations"] {
                    if let Some(Value::Array(arr)) = entity.get(field) {
                        for val in arr {
                            if let Some(s) = val.as_str() {
                                // More lenient matching for entities (check individual words)
                                let words: Vec<&str> = s.split_whitespace().collect();
                                let found = words.iter().any(|w| {
                                    source_lower.contains(&w.to_lowercase())
                                });
                                if !found {
                                    return Err(SkillError::HallucinationDetected(s.to_string()));
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    Ok(())
}

/// Parse skill output from LLM response
///
/// Expects JSON output. Returns error if output is not valid JSON
/// or doesn't match expected schema.
pub fn parse_skill_output(output: &str, target: ExtractionTarget) -> SkillResult<ExtractionOutput> {
    let trimmed = output.trim();

    // Try to parse as JSON
    let value: Value = serde_json::from_str(trimmed)
        .map_err(|e| SkillError::MalformedOutput(format!("invalid JSON: {}", e)))?;

    // Check it's an object
    if !value.is_object() {
        return Err(SkillError::MalformedOutput("output must be a JSON object".to_string()));
    }

    // Check target field exists
    if value.get(target.as_str()).is_none() {
        return Err(SkillError::SchemaViolation(format!(
            "output missing '{}' field",
            target.as_str()
        )));
    }

    Ok(ExtractionOutput { result: value })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_extraction_target_from_str() {
        assert_eq!(ExtractionTarget::from_str("email"), Some(ExtractionTarget::Email));
        assert_eq!(ExtractionTarget::from_str("URL"), Some(ExtractionTarget::Url));
        assert_eq!(ExtractionTarget::from_str("phone"), None);
    }

    #[test]
    fn test_input_validation() {
        let valid = ExtractionInput::new("hello@agent.rs", "email");
        assert!(valid.validate().is_ok());

        let empty = ExtractionInput::new("", "email");
        assert_eq!(empty.validate(), Err(SkillError::EmptyInput));

        let invalid_target = ExtractionInput::new("text", "phone");
        assert!(matches!(invalid_target.validate(), Err(SkillError::InvalidTarget(_))));
    }

    #[test]
    fn test_output_construction() {
        let emails = ExtractionOutput::emails(vec!["a@b.com".to_string()]);
        assert!(emails.has_target_field(ExtractionTarget::Email));
        assert!(!emails.has_target_field(ExtractionTarget::Url));
    }

    #[test]
    fn test_hallucination_detection() {
        let input = ExtractionInput::new("Contact us anytime", "email");
        let output = ExtractionOutput::emails(vec!["fake@example.com".to_string()]);

        let result = validate_extraction_output(&input, &output, ExtractionTarget::Email);
        assert!(matches!(result, Err(SkillError::HallucinationDetected(_))));
    }

    #[test]
    fn test_valid_extraction() {
        let input = ExtractionInput::new("Email: hello@agent.rs", "email");
        let output = ExtractionOutput::emails(vec!["hello@agent.rs".to_string()]);

        let result = validate_extraction_output(&input, &output, ExtractionTarget::Email);
        assert!(result.is_ok());
    }

    #[test]
    fn test_parse_skill_output() {
        let json = r#"{"email": ["test@example.com"]}"#;
        let result = parse_skill_output(json, ExtractionTarget::Email);
        assert!(result.is_ok());

        let invalid = "not json";
        let result = parse_skill_output(invalid, ExtractionTarget::Email);
        assert!(matches!(result, Err(SkillError::MalformedOutput(_))));

        let wrong_field = r#"{"url": "http://example.com"}"#;
        let result = parse_skill_output(wrong_field, ExtractionTarget::Email);
        assert!(matches!(result, Err(SkillError::SchemaViolation(_))));
    }

    #[test]
    fn test_skill_request_parsing() {
        let req = SkillRequest::new("extract", serde_json::json!({
            "text": "hello@test.com",
            "target": "email"
        }));

        assert!(req.is_extraction());
        let input = req.parse_extraction_input().unwrap();
        assert_eq!(input.text, "hello@test.com");
        assert_eq!(input.target, "email");
    }
}
