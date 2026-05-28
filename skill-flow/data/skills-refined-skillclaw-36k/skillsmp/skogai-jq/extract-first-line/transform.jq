# Extract first line from multiline string at path
# Usage: jq -f extract-first-line/transform.jq --arg path "field" input.json
#
# Arguments:
#   path: dot-separated path to string field (e.g., "data.message")
#
# Input: any JSON object containing string at path
# Output: string containing first line, or null if path doesn't exist or value is not a string

# Split path into array of keys and get string value
($path | split(".")) as $keys |
getpath($keys) as $value |

# Return first line if value exists and is a string, otherwise null
if $value != null and ($value | type) == "string" then
  # Handle empty string - return as-is
  if ($value | length) == 0 then
    $value
  else
    # Split by both Unix (\n) and Windows (\r\n) newlines
    # gsub normalizes \r\n to \n first, then split by \n
    $value | gsub("\r\n"; "\n") | split("\n") | .[0]
  end
else
  null
end
