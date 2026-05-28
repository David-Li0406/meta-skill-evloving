# Validate that fields have correct types
# Usage: jq -f validate-types/transform.jq --arg type_rules '{"name":"string","age":"number"}' input.json
#
# Arguments:
#   type_rules: JSON object mapping field paths to expected types (e.g., '{"user.name":"string","user.age":"number"}')
#               Supported types: "string", "number", "boolean", "null", "array", "object"
#
# Input: any JSON object
# Output: boolean (true if all fields match expected types, false if any mismatch or field missing)

# Parse type_rules argument as JSON object and capture input object
. as $input |
try ($type_rules | fromjson) catch {} as $rules |

# If rules are empty, return true (nothing to validate)
if ($rules | length) == 0 then
  true
else
  # Check each rule against the input object
  $rules | to_entries | all(
    .key as $path |
    .value as $expected_type |

    # Split path into keys and get value from input
    ($path | split(".")) as $keys |
    ($input | getpath($keys)) as $value |

    # Check if value exists and has correct type
    if $value == null and $expected_type != "null" then
      false
    else
      ($value | type) == $expected_type
    end
  )
end
