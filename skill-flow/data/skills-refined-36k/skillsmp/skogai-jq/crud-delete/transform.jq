# Delete value at path
# Usage: jq -f crud-delete/transform.jq --arg path "user.name" input.json
#
# Arguments:
#   path: dot-separated path to delete (e.g., "user.name")
#
# Input: any JSON object
# Output: modified object with value removed at path

# Split path into array of keys and delete value
($path | split(".")) as $keys |
delpaths([$keys])
