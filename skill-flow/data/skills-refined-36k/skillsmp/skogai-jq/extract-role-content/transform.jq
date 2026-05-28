# Extract content from messages filtered by role
# Usage: jq -f extract-role-content/transform.jq --arg array_path "messages" --arg role "user" input.json
#
# Arguments:
#   array_path: name of the field containing the messages array (e.g., "messages")
#   role: role to filter by (e.g., "user", "assistant", "system")
#
# Input: object containing a messages array
# Output: array of content strings from messages matching the role

# Get the array from the specified path
getpath([$array_path]) as $array |

# If array exists and is an array, filter by role and extract content
if ($array | type) == "array" then
  $array
  | map(select(
      (type == "object") and
      (.role == (try ($role | fromjson) catch $role))
    ))
  | map(
      if .content != null then .content else null end
    )
else
  []
end
