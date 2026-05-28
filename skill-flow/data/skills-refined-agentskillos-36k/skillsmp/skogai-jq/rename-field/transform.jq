# Rename a field from old path to new path
# Usage: jq -f rename-field/transform.jq --arg old_path "user.name" --arg new_path "user.fullName" input.json
#
# Arguments:
#   old_path: dot-separated path to the field to rename (e.g., "user.name")
#   new_path: dot-separated path for the new field name (e.g., "user.fullName")
#
# Input: any JSON object
# Output: modified object with field renamed (copied to new location, old location deleted)

# Split paths into array of keys
($old_path | split(".")) as $old_keys |
($new_path | split(".")) as $new_keys |

# Get value at old path
getpath($old_keys) as $value |

# Set value at new path, then delete old path
setpath($new_keys; $value) |
delpaths([$old_keys])
