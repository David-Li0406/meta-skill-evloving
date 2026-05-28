# Check if path exists in object
# Usage: jq -f crud-has/transform.jq --arg path "user.name" input.json
#
# Arguments:
#   path: dot-separated path to check (e.g., "user.name")
#
# Input: any JSON object
# Output: boolean (true if path exists, false otherwise)

# Split path into array of keys and check if path exists
# Note: This checks if the KEY exists, not if the value is non-null
# A path with a null value still exists (e.g., {"user": {"name": null}})
($path | split(".")) as $keys |
reduce $keys[] as $key (
  {obj: ., exists: true};
  if .exists then
    if (.obj | type) == "object" and (.obj | has($key)) then
      {obj: .obj[$key], exists: true}
    else
      {obj: null, exists: false}
    end
  else
    .
  end
) | .exists
