# Apply a field extraction or simple calculation to each element in an array
# Usage: jq -f map-transform/transform.jq --arg array_path "items" --arg field "name" [--arg operation "multiply" --arg operand "1.1"] input.json
#
# Arguments:
#   array_path: dot-separated path to the array field (e.g., "data.items")
#   field: field name to extract or transform from each element
#   operation: optional operation to apply (multiply, add, subtract, divide, uppercase, lowercase, tostring, tonumber)
#   operand: operand for arithmetic operations (required for multiply, add, subtract, divide)
#
# Input: object containing an array at the specified path
# Output: modified object with transformation applied to array elements

($ARGS.named.array_path // "items") as $arrayPath |
($ARGS.named.field // ".") as $fieldName |
($ARGS.named.operation // "none") as $operation |
($ARGS.named.operand // "0") as $operand |

# Split the array path into keys
($arrayPath | split(".")) as $keys |

# Get the array from the specified path
getpath($keys) as $array |

# Type-check: ensure we have an array
if ($array | type) == "array" then
  setpath($keys;
    $array | map(
      # Extract the field value
      (if type == "object" then .[$fieldName] else . end) as $value |

      # Apply the operation if specified
      if $operation == "multiply" then
        try ($value * ($operand | tonumber)) catch null
      elif $operation == "add" then
        try ($value + ($operand | tonumber)) catch null
      elif $operation == "subtract" then
        try ($value - ($operand | tonumber)) catch null
      elif $operation == "divide" then
        try ($value / ($operand | tonumber)) catch null
      elif $operation == "uppercase" then
        try ($value | ascii_upcase) catch $value
      elif $operation == "lowercase" then
        try ($value | ascii_downcase) catch $value
      elif $operation == "tostring" then
        try ($value | tostring) catch null
      elif $operation == "tonumber" then
        try ($value | tonumber) catch null
      else
        $value
      end
    )
  )
else
  # If not an array, return the input unchanged
  .
end
