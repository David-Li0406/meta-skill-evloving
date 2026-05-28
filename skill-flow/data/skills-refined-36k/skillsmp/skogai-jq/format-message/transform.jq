# Format message object as string using template with field placeholders
# Usage: jq -f format-message/transform.jq --arg template "{role}: {content}" input.json
#
# Arguments:
#   template: string with {field} placeholders (e.g., "{role}: {content}")
#
# Input: any JSON object
# Output: formatted string with {field} replaced by field values

# Capture the input object first
. as $input |
$template as $tmpl |

# Replace all {field} placeholders with actual values
# Strategy: find all {field} patterns and replace each with getpath value
reduce (
  # Find all {field} patterns in template
  $tmpl | scan("\\{([^}]+)\\}") | .[0]
) as $field (
  $tmpl;
  # For each field, get value from input object and replace placeholder
  ($field | split(".")) as $keys |
  ($input | getpath($keys)) as $value |

  # Replace {field} with string representation of value
  if $value != null then
    gsub("\\{" + $field + "\\}"; $value | tostring)
  else
    # Leave placeholder or replace with empty string
    gsub("\\{" + $field + "\\}"; "")
  end
)
