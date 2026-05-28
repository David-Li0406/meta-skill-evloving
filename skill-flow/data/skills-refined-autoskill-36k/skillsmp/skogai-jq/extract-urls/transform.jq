# Extract all URLs from a string at specified path
# Usage: jq -f extract-urls/transform.jq --arg path "text" input.json
#
# Arguments:
#   path: dot-separated path to string field (e.g., "content.text")
#
# Input: any JSON object containing string at path
# Output: array of URL strings found (http://, https://, ftp://), or empty array if none found

# Split path into array of keys and get string value
($path | split(".")) as $keys |
getpath($keys) as $value |

# Return array of URLs or empty array
if $value != null and ($value | type) == "string" then
  # Regex pattern for URLs: http://, https://, ftp://
  # Matches: scheme://domain.tld/path?query#fragment
  # Excludes common terminators: ), ], >, comma, period at end
  # Case insensitive flag: "i"
  [$value | scan("(?:https?|ftp)://[^\\s<>\"{}|\\\\^`\\[\\]()]+"; "i")]
else
  []
end
