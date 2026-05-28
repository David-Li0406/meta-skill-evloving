# Validate that all required fields exist in object
# Usage: jq -f validate-required/transform.jq --arg required_fields '["user.name","user.email"]' input.json
#
# Arguments:
#   required_fields: JSON array string of dot-separated paths (e.g., '["name","user.email"]')
#
# Input: any JSON object
# Output: boolean (true if all required fields exist, false if any are missing)

# Parse required_fields argument as JSON array
($ARGS.named.required_fields | fromjson) as $fields |

# Capture the input object
. as $input |

# Check if all required fields exist
# Note: This checks if the KEY exists, not if the value is non-null
# A field with a null/false/0/"" value still exists and passes validation
if ($fields | length) == 0 then
  # Empty required list always passes
  true
else
  # Check each field for existence
  $fields | map(
    split(".") as $keys |
    reduce $keys[] as $key (
      {obj: $input, exists: true};
      if .exists then
        if (.obj | type) == "object" and (.obj | has($key)) then
          {obj: .obj[$key], exists: true}
        else
          {obj: null, exists: false}
        end
      else
        .
      end
    ) | .exists
  ) | all
end
