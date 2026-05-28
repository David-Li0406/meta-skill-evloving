# Add a new field to an object at a specified path
# Usage: jq -f add-field/transform.jq --arg path "user" --arg field_name "email" --arg value "user@example.com" input.json
#
# Arguments:
#   path: dot-separated path to the object where field should be added (e.g., "user.profile")
#   field_name: name of the field to add
#   value: value to set for the field
#
# Input: any JSON object
# Output: modified object with new field added at specified path

# Split path into array of keys
($path | split(".")) as $path_keys |

# Navigate to target object and add field
if $path_keys == [""] then
  # Root level - add field directly
  .[$field_name] = $value
else
  # Nested path - need to get existing object and add field
  getpath($path_keys) as $target_obj |

  # Build new object with added field
  if ($target_obj | type) == "object" or $target_obj == null then
    setpath($path_keys + [$field_name]; $value)
  else
    # Target is not an object - cannot add field
    .
  end
end
