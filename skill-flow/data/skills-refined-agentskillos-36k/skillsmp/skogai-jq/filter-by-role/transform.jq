# Filter messages by role field
# Usage: jq -f filter-by-role/transform.jq --arg array_path "messages" --arg role "user" input.json
#
# Arguments:
#   array_path: name of the field containing the messages array (e.g., "messages")
#   role: role to filter by (e.g., "user", "assistant", "system")
#
# Input: object containing a messages array
# Output: object with filtered messages array containing only messages matching the role

# Get the array from the specified path
getpath([$array_path]) as $array |

# If array exists and is an array, filter by role
if ($array | type) == "array" then
  setpath(
    [$array_path];
    $array | map(select(
      (type == "object") and
      (.role == (try ($role | fromjson) catch $role))
    ))
  )
else
  .
end
