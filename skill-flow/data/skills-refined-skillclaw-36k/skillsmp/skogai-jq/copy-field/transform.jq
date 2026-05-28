# Copy value from source path to destination path
# Usage: jq -f copy-field/transform.jq --arg source_path "user.name" --arg dest_path "profile.username" input.json
#
# Arguments:
#   source_path: dot-separated path to source value (e.g., "user.name")
#   dest_path: dot-separated path where to copy value (e.g., "profile.username")
#
# Input: any JSON object
# Output: object with value copied from source to destination (creates intermediate objects as needed)

# Split paths into arrays of keys
($source_path | split(".")) as $source_keys |
($dest_path | split(".")) as $dest_keys |

# Get value from source path
getpath($source_keys) as $value |

# Set value at destination path
setpath($dest_keys; $value)
