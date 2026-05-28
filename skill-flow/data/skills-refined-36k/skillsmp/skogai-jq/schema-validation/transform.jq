# Validate JSON against a schema with type and required field checks
# Usage: jq -f schema-validation/transform.jq --arg schema '{"required":["name"],"types":{"name":"string"}}' input.json
#
# Arguments:
#   schema: JSON object string with validation rules:
#           {
#             "required": ["field1", "nested.field2"],  // optional array of required field paths
#             "types": {"field1": "string", "field2": "number"}  // optional type mapping
#           }
#           Supported types: "string", "number", "boolean", "null", "array", "object"
#
# Input: any JSON object to validate
# Output: object with validation results:
#         {
#           "valid": boolean,
#           "errors": array of error messages (empty if valid)
#         }

# Parse schema argument and capture input
. as $input |
try ($ARGS.named.schema | fromjson) catch {} as $schema |

# Initialize validation results
{
  valid: true,
  errors: []
} as $init |

# Validate required fields
(
  if ($schema.required // [] | length) > 0 then
    ($schema.required // []) | map(
      split(".") as $keys |
      reduce $keys[] as $key (
        {obj: $input, exists: true, path: ""};
        if .exists then
          if (.path == "") then
            {path: $key} + (
              if ((.obj | type) == "object" and (.obj | has($key))) then
                {obj: .obj[$key], exists: true}
              else
                {obj: null, exists: false}
              end
            )
          else
            {path: (.path + "." + $key)} + (
              if ((.obj | type) == "object" and (.obj | has($key))) then
                {obj: .obj[$key], exists: true}
              else
                {obj: null, exists: false}
              end
            )
          end
        else
          .
        end
      ) |
      if .exists then
        null
      else
        "Required field '\(.path)' is missing"
      end
    ) | map(select(. != null))
  else
    []
  end
) as $required_errors |

# Validate types
(
  if ($schema.types // {} | length) > 0 then
    ($schema.types // {}) | to_entries | map(
      .key as $path |
      .value as $expected_type |
      ($path | split(".")) as $keys |
      ($input | getpath($keys)) as $value |

      if $value == null and $expected_type != "null" then
        "Field '\($path)' is null, expected type '\($expected_type)'"
      elif ($value | type) != $expected_type then
        "Field '\($path)' has type '\($value | type)', expected '\($expected_type)'"
      else
        null
      end
    ) | map(select(. != null))
  else
    []
  end
) as $type_errors |

# Combine errors and determine validity
($required_errors + $type_errors) as $all_errors |
{
  valid: ($all_errors | length) == 0,
  errors: $all_errors
}
