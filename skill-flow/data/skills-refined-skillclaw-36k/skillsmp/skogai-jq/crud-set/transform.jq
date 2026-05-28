# Set value at path
# Usage: jq -f crud-set/transform.jq --arg path "user.name" --arg value "newvalue" input.json
#
# Arguments:
#   path: dot-separated path where to set value (e.g., "user.name")
#   value: value to set (string)
#
# Input: any JSON object
# Output: modified object with value set at path

# Split path into array of keys and set value
($path | split(".")) as $keys |
setpath($keys; $value)
