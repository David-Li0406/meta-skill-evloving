# Normalize timestamps to ISO 8601 format
# Usage: jq -f normalize-timestamp/transform.jq --arg path "created_at" input.json
#
# Arguments:
#   path: dot-separated path to timestamp field (e.g., "user.created_at")
#
# Input: object containing a timestamp field (ISO 8601 string, Unix timestamp number, or date-only string)
# Output: object with timestamp normalized to ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)

# Split path into array of keys and get value
($path | split(".")) as $keys |
getpath($keys) as $value |

# Helper function to normalize value to ISO 8601
($value |
  if . == null then
    null
  elif type == "string" then
    # Check if already ISO 8601 format
    if test("^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(\\.\\d{1,9})?(Z|[+-]\\d{2}:\\d{2})?$") then
      # Already full ISO 8601, keep as is
      .
    elif test("^\\d{4}-\\d{2}-\\d{2}$") then
      # Date-only format, add time component
      . + "T00:00:00Z"
    elif test("^\\d+$") then
      # String containing unix timestamp (seconds)
      (tonumber | todate)
    elif test("^\\d+\\.\\d+$") then
      # String containing unix timestamp with decimals (seconds.milliseconds)
      ((tonumber | floor) | todate)
    else
      # Not a recognized format, keep original
      .
    end
  elif type == "number" then
    # Unix timestamp handling
    if . > 10000000000 then
      # Milliseconds (13+ digits) - convert to seconds first
      ((. / 1000) | floor | todate)
    else
      # Seconds (10 digits or less)
      (. | floor | todate)
    end
  else
    # Other types (boolean, array, object) - return null
    null
  end
) as $normalized |

# Set the normalized value back at the path
setpath($keys; $normalized)
