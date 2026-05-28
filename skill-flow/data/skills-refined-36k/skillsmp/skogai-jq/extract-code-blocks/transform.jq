# Extract code blocks from markdown text
# Usage: jq -f extract-code-blocks/transform.jq --arg path "content" input.json
#
# Arguments:
#   path: dot-separated path to string field containing markdown (e.g., "data.content")
#
# Input: any JSON object containing string at path
# Output: array of code block strings (with ``` delimiters), or empty array if none found

# Split path into array of keys and get string value
($path | split(".")) as $keys |
getpath($keys) as $value |

# Return array of code blocks if value exists and is a string, otherwise empty array
if $value != null and ($value | type) == "string" then
  # Extract all code blocks matching ```...``` pattern (including newlines)
  [$value | scan("```[^`]*```"; "s")]
else
  []
end
