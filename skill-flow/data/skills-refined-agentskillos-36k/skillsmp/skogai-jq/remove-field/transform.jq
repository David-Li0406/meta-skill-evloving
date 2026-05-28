# Remove a field from an object at a specified path
# Usage: jq -f remove-field/transform.jq --arg path "user.email" input.json
#
# Arguments:
#   path: dot-separated path to field to remove (e.g., "user.profile.age")
#
# Input: any JSON object
# Output: object with field removed at specified path

# Split path into array of keys and remove the field
($path | split(".")) as $keys |
delpaths([$keys])
