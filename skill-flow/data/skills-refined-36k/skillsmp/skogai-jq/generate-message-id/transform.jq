# Generate unique message ID from content hash or timestamp
# Usage: jq -f generate-message-id/transform.jq --arg id_field "id" [--arg strategy "hash|timestamp"] input.json
#
# Arguments:
#   id_field: dot-separated path where ID should be stored (e.g., "message.id" or "id")
#   strategy: "hash" (default, content-based), "timestamp" (current time), or "hybrid" (timestamp + short hash)
#
# Input: any JSON object
# Output: object with ID field added/updated at specified path

($ARGS.named.id_field // "id") as $id_field |
($ARGS.named.strategy // "hash") as $strategy |
($id_field | split(".")) as $keys |

# Generate ID based on strategy
(
  if $strategy == "timestamp" then
    # Timestamp-based ID (ISO 8601 format with milliseconds)
    now | todate | gsub("[:-]"; "") | gsub("T"; "-") | gsub("\\."; "-") | split("Z")[0]
  elif $strategy == "hybrid" then
    # Hybrid: timestamp + short content hash
    (now | todate | split("T")[0] | gsub("-"; "")) + "-" + (tojson | @base64 | .[0:8])
  else
    # Default: hash-based ID (content hash using base64 encoding)
    # Use base64 of JSON representation (22 chars for better uniqueness)
    "msg-" + (tojson | @base64 | gsub("[+/=]"; "") | .[0:22])
  end
) as $generated_id |

# Set the ID at the specified path
setpath($keys; $generated_id)
