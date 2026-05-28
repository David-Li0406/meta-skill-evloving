# Filter array of objects by date field within a range
# Usage: jq -f filter-by-date-range/transform.jq --arg array_path "items" --arg date_field "created_at" --arg start_date "2024-01-01" --arg end_date "2024-12-31" input.json
#
# Arguments:
#   array_path: dot-separated path to array field (e.g., "data.items")
#   date_field: name of the date field within array items
#   start_date: ISO 8601 start date (optional, format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ)
#   end_date: ISO 8601 end date (optional, format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ)
#
# Input: object containing an array at the specified path
# Output: object with filtered array containing only items within date range

# Parse optional arguments
($ARGS.named.start_date // "") as $start |
($ARGS.named.end_date // "") as $end |

# Split path into array of keys and get array value
($array_path | split(".")) as $keys |
getpath($keys) as $array |

# Type-check: ensure field is an array before processing
if ($array | type) != "array" then
  .
else
  setpath(
    $keys;
    $array | map(
      select(
        # Get the date value from the specified field
        .[$date_field] as $date_value |

        # Skip if date field is missing or null
        if $date_value == null then
          false
        else
          # Try to validate it's a string (ISO 8601 dates are strings)
          if ($date_value | type) != "string" then
            false
          else
            # Check date range
            (
              # Check start date if provided
              (if $start == "" then true else $date_value >= $start end)
              and
              # Check end date if provided
              (if $end == "" then true else $date_value <= $end end)
            )
          end
        end
      )
    )
  )
end
