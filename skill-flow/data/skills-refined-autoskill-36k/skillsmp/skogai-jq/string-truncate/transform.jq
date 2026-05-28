# Truncate string at path to maximum length, optionally adding ellipsis
# Usage: jq -f string-truncate/transform.jq --arg path "data" --argjson max_length 10 [--arg ellipsis "true"] input.json
#
# Arguments:
#   path: dot-separated path to string field (e.g., "user.bio")
#   max_length: maximum number of characters to keep (passed as JSON number)
#   ellipsis: (optional) "true" to add "..." to truncated strings (default: "false")
#
# Input: any JSON object containing string at path
# Output: modified object with truncated string at path
#
# Note: When ellipsis is enabled, the ellipsis is included in the max_length count,
#       so a 10-character limit with ellipsis will show 7 chars + "..."

($path | split(".")) as $keys |
getpath($keys) as $value |
($ARGS.named.ellipsis // "false") as $ellipsis_mode |

if $value != null and ($value | type) == "string" then
  # Calculate length of string
  ($value | length) as $len |

  if $len <= $max_length then
    # No truncation needed
    .
  elif $ellipsis_mode == "true" then
    # Truncate with ellipsis (ellipsis counts toward max_length)
    if $max_length >= 3 then
      setpath($keys; ($value[0:($max_length - 3)] + "..."))
    else
      # If max_length < 3, just use dots
      setpath($keys; ("..." | .[0:$max_length]))
    end
  else
    # Truncate without ellipsis
    setpath($keys; $value[0:$max_length])
  end
else
  # Return unchanged if path doesn't exist or value is not a string
  .
end
