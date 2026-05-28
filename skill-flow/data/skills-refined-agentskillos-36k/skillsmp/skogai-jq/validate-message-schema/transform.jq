# Validate message object schema (role, content, timestamp fields)
# Usage: jq -f validate-message-schema/transform.jq input.json
#
# Arguments:
#   None (validates standard message schema)
#
# Input: any JSON object to validate as a message
# Output: object with {valid: boolean, errors: [string]} - valid is true if message matches schema, errors contains list of validation failures

# Define the message schema requirements
{
  role: {required: true, type: "string", enum: ["user", "assistant", "system"]},
  content: {required: true, type: "string"},
  timestamp: {required: false, type: "string"}
} as $schema |

# Capture input object
. as $input |

# Validate input is an object
if ($input | type) != "object" then
  {valid: false, errors: ["Input must be an object"]}
else
  # Check all schema requirements
  $schema | to_entries | reduce .[] as $field (
    {valid: true, errors: []};

    $field.key as $fieldname |
    $field.value as $rules |

    # Check if field exists
    if $rules.required and ($input | has($fieldname) | not) then
      .valid = false |
      .errors += ["Required field '\($fieldname)' is missing"]
    elif ($input | has($fieldname)) then
      # Field exists, check type
      ($input[$fieldname] | type) as $actualtype |
      if $actualtype != $rules.type then
        .valid = false |
        .errors += ["Field '\($fieldname)' has wrong type (expected \($rules.type), got \($actualtype))"]
      # If field has enum constraint, validate value
      elif $rules | has("enum") then
        if ($rules.enum | map(. == $input[$fieldname]) | any) | not then
          .valid = false |
          .errors += ["Field '\($fieldname)' has invalid value '\($input[$fieldname])' (must be one of: \($rules.enum | join(", ")))"]
        else
          .
        end
      else
        .
      end
    else
      # Optional field not present - OK
      .
    end
  ) |

  # Check for extra fields not in schema
  ($input | keys) as $inputkeys |
  ($schema | keys) as $schemakeys |
  ($inputkeys - $schemakeys) as $extrakeys |

  if ($extrakeys | length) > 0 then
    .valid = false |
    .errors += ["Unexpected fields: \($extrakeys | join(", "))"]
  else
    .
  end
end
