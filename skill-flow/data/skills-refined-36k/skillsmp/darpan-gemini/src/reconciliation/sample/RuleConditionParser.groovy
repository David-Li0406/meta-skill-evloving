package reconciliation.sample

import java.util.regex.Matcher
import java.util.regex.Pattern

/**
 * Parses simplified, human-readable rule conditions into Drools DRL syntax.
 */
class RuleConditionParser {

    // Map of simple operators to DRL/Java operators
    private static final Map<String, String> OPERATOR_MAP = [
        'is': '==',
        'equals': '==',
        'is not': '!=',
        'not equals': '!=',
        'greater than': '>',
        '>': '>',
        'less than': '<',
        '<': '<',
        'greater than or equals': '>=',
        '>=': '>=',
        'less than or equals': '<=',
        '<=': '<='
    ]

    /**
     * Parses a single line condition.
     * Example: "status is 'Blocked'" -> 'this["status"] == "Blocked"'
     * Assumption: We are operating on a Map<String, Object> fact.
     */
    static String parseCondition(String condition) {
        if (!condition) return ""
        
        // Basic pattern: [Field] [Operator] [Value]
        // Value can be string ('value' or "value") or number
        // Simple regex approach for now
        
        // Split by first occurrence of known operators?
        // Let's iterate through operators to find a match.
        // Longest match first to avoid partial matches (e.g. ">" vs ">=")
        
        List<String> sortedOps = OPERATOR_MAP.keySet().sort { -it.length() }
        
        for (String op : sortedOps) {
            // Regex to match "Field [op] Value" with spaces
            // \s+ ensures spaces around the operator word, but symbols might be tight? 
            // For words like "is", we need word boundaries \b
            
            String regexOp
            if (op.matches("[a-zA-Z\\s]+")) {
                regexOp = "\\b${op}\\b"
            } else {
                regexOp = Pattern.quote(op)
            }
            
            // Pattern: start, capture group 1 (field), op, capture group 2 (value), end
            Pattern pattern = Pattern.compile("^\\s*(.+?)\\s+" + regexOp + "\\s+(.+)\\s*\$", Pattern.CASE_INSENSITIVE)
            Matcher matcher = pattern.matcher(condition)
            
            if (matcher.find()) {
                String field = matcher.group(1).trim()
                String value = matcher.group(2).trim()
                String drlOp = OPERATOR_MAP[op]
                
                return formatDrl(field, drlOp, value)
            }
        }
        
        // Specialized operators
        if (condition.toLowerCase().contains(" contains ")) {
            return parseContains(condition)
        }

        return "" // OR throw exception?
    }
    
    private static String formatDrl(String field, String operator, String value) {
        // Handle field needing quotes if map access?
        // Drools map property access: this["field"] or field (if property reactive but Map isn't usually)
        // We used: m : java.util.Map( this["status"] == "Blocked" ) in the test.
        
        // Clean value quotes if present
        // If value is a string literal, ensure it is quoted consistently.
        // If number, leave as is.
        
        return "this[\"${field}\"] ${operator} ${value}"
    }

    private static String parseContains(String condition) {
         Pattern pattern = Pattern.compile("^\\s*(.+?)\\s+contains\\s+(.+)\\s*\$", Pattern.CASE_INSENSITIVE)
         Matcher matcher = pattern.matcher(condition)
         if (matcher.find()) {
             String field = matcher.group(1).trim()
             String value = matcher.group(2).trim()
             // "field".contains("value") logic? 
             // Depending on if field is a list or string.
             // Safe approach: this["field"] != null && this["field"].toString().contains(value)
             return "this[\"${field}\"] != null && this[\"${field}\"].toString().contains(${value})"
         }
         return ""
    }
}
