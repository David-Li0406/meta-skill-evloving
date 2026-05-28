# Deep merge two objects recursively
# Usage: jq -f crud-merge/transform.jq --arg source_path "path.to.source" --arg target_path "path.to.target" input.json
#
# Arguments:
#   source_path: dot-separated path to source object to merge from
#   target_path: dot-separated path to target object to merge into
#
# Input: any JSON object containing both source and target paths
# Output: modified object with source merged into target at target_path

def deep_merge(source; target):
  if (source | type) == "object" and (target | type) == "object" then
    # Get all unique keys from both objects and merge values
    ([(source | keys[]), (target | keys[])] | unique) as $all_keys |
    ($all_keys | map(. as $key |
      if (source | has($key)) and (target | has($key)) then
        {key: $key, value: deep_merge(source[$key]; target[$key])}
      elif source | has($key) then
        {key: $key, value: source[$key]}
      else
        {key: $key, value: target[$key]}
      end
    ) | from_entries)
  else
    source
  end;

($source_path | split(".")) as $source_keys |
($target_path | split(".")) as $target_keys |
getpath($source_keys) as $source |
getpath($target_keys) as $target |

if $source == null then
  .
elif $target == null then
  setpath($target_keys; $source)
else
  setpath($target_keys; deep_merge($source; $target))
end
