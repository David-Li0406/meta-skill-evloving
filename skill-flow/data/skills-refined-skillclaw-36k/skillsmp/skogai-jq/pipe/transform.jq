# Chain multiple transformations in sequence (pipe)
# Usage: jq -f pipe/transform.jq --argjson steps '[...]' input.json
#
# Arguments:
#   steps: JSON array of transformation steps
#          Each step: {"op": "set|delete", "path": "x.y.z", "value": "val" (for set)}
#
# Input: any JSON object
# Output: transformed object after applying all steps in sequence

# Get steps array from argument
($ARGS.named.steps // "[]") as $stepsArg |

# Parse steps argument (handle both JSON string and direct JSON)
(try ($stepsArg | fromjson) catch $stepsArg) as $steps |

# Type-check: ensure steps is an array
if ($steps | type) != "array" then
  # If not an array, return input unchanged
  .
elif ($steps | length) == 0 then
  # Empty pipeline: return input unchanged
  .
else
  # Apply each step sequentially using reduce
  reduce $steps[] as $step (
    .;  # Start with current input
    . as $current |

    # Validate step is an object
    if ($step | type) != "object" then
      $current
    # Check if op is specified
    elif ($step.op // "") == "" then
      $current
    # Check if path is specified (required for all ops)
    elif ($step.path // "") == "" then
      $current
    else
      # Parse the path
      ($step.path | split(".")) as $keys |

      # Execute the operation
      if $step.op == "set" then
        # Set operation: set value at path
        # Parse value if it's a JSON string, otherwise use as-is
        (try ($step.value | fromjson) catch $step.value) as $val |
        setpath($keys; $val)
      elif $step.op == "delete" then
        # Delete operation: remove path
        delpaths([$keys])
      else
        # Unknown operation, pass through unchanged
        $current
      end
    end
  )
end
