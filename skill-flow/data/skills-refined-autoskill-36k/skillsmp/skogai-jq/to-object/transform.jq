# Convert value to object
# Usage: jq -f to-object/transform.jq --arg path "data.items" input.json
#
# Arguments:
#   path: dot-separated path to value to convert (e.g., "data.items")
#
# Input: any JSON object
# Output: object with value at path converted to object
#
# Conversion rules:
#   - object: pass through unchanged
#   - array of [key, value] pairs: convert to object
#   - array of {"key": k, "value": v} objects: convert to object
#   - null: returns empty object {}
#   - other types (string, number, boolean, empty array): return empty object {}

# Split path into array of keys
($path | split(".")) as $keys |

# Get the value at path
getpath($keys) as $value |

# Determine the converted value based on type
if ($value | type) == "object" then
  # Already an object, pass through
  .
elif $value == null then
  # Null becomes empty object
  setpath($keys; {})
elif ($value | type) == "array" then
  # Try to convert array to object
  if ($value | length) == 0 then
    # Empty array becomes empty object
    setpath($keys; {})
  elif ($value | all(type == "array" and length == 2)) then
    # Array of [key, value] pairs
    setpath($keys; $value | map({key: .[0] | tostring, value: .[1]}) | from_entries)
  elif ($value | all(type == "object" and has("key") and has("value"))) then
    # Array of {key: k, value: v} objects
    setpath($keys; $value | from_entries)
  else
    # Other arrays become empty object
    setpath($keys; {})
  end
else
  # Other types (string, number, boolean) become empty object
  setpath($keys; {})
end
