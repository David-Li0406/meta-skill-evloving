# Replace pattern in string at path with replacement
# Usage: jq -f string-replace/transform.jq --arg path "data" --arg pattern "old" --arg replacement "new" input.json
#
# Arguments:
#   path: dot-separated path to string field (e.g., "user.name")
#   pattern: regex pattern to replace (e.g., "\\d+" for digits)
#   replacement: string to replace matches with (e.g., "X")
#
# Input: any JSON object containing string at path
# Output: modified object with replacements applied, or original if path doesn't exist/is not a string

# Split path into array of keys and get value
($path | split(".")) as $keys |
getpath($keys) as $value |

# If value exists and is a string, apply replacement and update object
if $value != null and ($value | type) == "string" then
  setpath($keys; ($value | gsub($pattern; $replacement)))
else
  # Return original object unchanged if path doesn't exist or value is not a string
  .
end
