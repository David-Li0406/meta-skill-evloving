# Get value at path with optional default
# Usage: jq -f crud-get/transform.jq --arg path "user.name" [--arg default "value"] input.json
#
# Arguments:
#   path: dot-separated path to value (e.g., "user.name")
#   default: value to return if path doesn't exist (optional, use empty string to skip)
#
# Input: any JSON object
# Output: value at path, or default if not found

# Split path into array of keys and get value
($path | split(".")) as $keys |
getpath($keys) as $value |

# Return value if found, otherwise default (if provided and non-empty), otherwise null
if $value != null then
  $value
elif ($ARGS.named.default // "") != "" then
  $ARGS.named.default
else
  null
end
