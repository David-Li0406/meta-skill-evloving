# Select only specified fields from an object
# Usage: jq -f pick-fields/transform.jq --arg fields "field1,field2,field3" input.json
#
# Arguments:
#   fields: comma-separated list of field names to keep (e.g., "name,email,age")
#
# Input: any JSON object
# Output: new object containing only the specified fields

# Split fields by comma into an array of field names
($fields | split(",") | map(gsub("^ +| +$"; ""))) as $fieldNames |

# Create new object with only the specified fields
. as $input |
reduce $fieldNames[] as $field (
  {};
  . + {($field): $input[$field]}
)
