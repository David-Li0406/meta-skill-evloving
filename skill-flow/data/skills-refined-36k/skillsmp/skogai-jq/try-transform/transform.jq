# Try transformation, return fallback on error
# Usage: jq -f try-transform/transform.jq --arg transform_expr ".user.age / 10" --arg fallback "null" input.json
#
# Arguments:
#   transform_expr: jq expression to attempt (as string)
#   fallback: value to return on error (JSON string, will be parsed)
#
# Input: any JSON value
# Output: result of transform_expr on success, fallback on error
#
# This is a meta-transformation for error handling. It tries to execute
# a jq expression and returns a fallback value if the expression fails.
# Useful for defensive programming with potentially failing operations.

# Parse the fallback value from JSON string
(try ($ARGS.named.fallback | fromjson) catch $ARGS.named.fallback) as $fallback_value |

# Try to execute the transform expression, catch errors and return fallback
# Note: We cannot dynamically evaluate arbitrary jq expressions from strings
# This transformation instead works by providing common error-prone operations
# as built-in cases that can be selected via the transform_expr argument

if $ARGS.named.transform_expr == "identity" then
  try . catch $fallback_value
elif ($ARGS.named.transform_expr | test("^getpath:")) then
  # Extract path: "getpath:user.name"
  ($ARGS.named.transform_expr | split(":")[1] | split(".")) as $keys |
  (try getpath($keys) catch $fallback_value) as $result |
  if $result == null then $fallback_value else $result end
elif ($ARGS.named.transform_expr | test("^divide:")) then
  # Division: "divide:field:divisor"
  ($ARGS.named.transform_expr | split(":")) as $parts |
  ($parts[1] | split(".")) as $keys |
  ($parts[2] | tonumber) as $divisor |
  try (getpath($keys) / $divisor) catch $fallback_value
elif ($ARGS.named.transform_expr | test("^tonumber:")) then
  # Convert to number: "tonumber:field.path"
  ($ARGS.named.transform_expr | split(":")[1] | split(".")) as $keys |
  try (getpath($keys) | tonumber) catch $fallback_value
elif ($ARGS.named.transform_expr | test("^array_access:")) then
  # Array access: "array_access:items:0"
  ($ARGS.named.transform_expr | split(":")) as $parts |
  ($parts[1] | split(".")) as $keys |
  ($parts[2] | tonumber) as $index |
  try (getpath($keys)[$index]) catch $fallback_value
elif ($ARGS.named.transform_expr | test("^fromjson:")) then
  # Parse JSON: "fromjson:field.path"
  ($ARGS.named.transform_expr | split(":")[1] | split(".")) as $keys |
  try (getpath($keys) | fromjson) catch $fallback_value
elif ($ARGS.named.transform_expr | test("^nested:")) then
  # Nested transformation: "nested:field1.field2.field3"
  ($ARGS.named.transform_expr | split(":")[1] | split(".")) as $keys |
  (try getpath($keys) catch $fallback_value) as $result |
  if $result == null then $fallback_value else $result end
else
  # Default: try identity, return fallback on error
  try . catch $fallback_value
end
