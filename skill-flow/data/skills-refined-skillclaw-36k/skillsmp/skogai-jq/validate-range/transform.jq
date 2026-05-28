# Validate that a numeric value falls within a specified range
# Usage: jq -f validate-range/transform.jq --arg path "user.age" [--arg min "0"] [--arg max "100"] [--arg exclusive "false"] input.json
#
# Arguments:
#   path: dot-separated path to the numeric field to validate (e.g., "user.age")
#   min: minimum value (optional, unbounded if not specified)
#   max: maximum value (optional, unbounded if not specified)
#   exclusive: "true" for exclusive bounds (< and >), "false" for inclusive (≤ and ≥), default: "false"
#
# Input: any JSON object
# Output: boolean (true if value is within range or path doesn't exist, false if out of range or not a number)

# Get arguments with defaults
($path | split(".")) as $keys |
($ARGS.named.min // null) as $min_str |
($ARGS.named.max // null) as $max_str |
($ARGS.named.exclusive // "false") as $exclusive_str |

# Parse min/max as numbers (null if not provided or invalid)
(if $min_str then try ($min_str | tonumber) catch null else null end) as $min |
(if $max_str then try ($max_str | tonumber) catch null else null end) as $max |

# Parse exclusive as boolean
($exclusive_str == "true") as $exclusive |

# Get value at path
getpath($keys) as $value |

# Validate:
# - If path doesn't exist (value is null and min/max not set), return true
# - If value exists but is not a number, return false
# - If value is a number, check range
if $value == null then
  # Path doesn't exist - return true (nothing to validate)
  true
elif ($value | type) != "number" then
  # Value exists but is not a number - return false
  false
else
  # Value is a number - check range
  if $exclusive then
    # Exclusive bounds (< and >)
    (if $min != null then $value > $min else true end) and
    (if $max != null then $value < $max else true end)
  else
    # Inclusive bounds (≤ and ≥)
    (if $min != null then $value >= $min else true end) and
    (if $max != null then $value <= $max else true end)
  end
end
