# Generate test cases from transformation schema
# Usage: jq -f test-generator/transform.jq [--arg format "bash"] input-schema.json
#
# Arguments:
#   format: output format ("bash" or "json", defaults to "bash")
#
# Input: transformation schema.json with name, description, input, args, output, examples
# Output: array of test case objects or bash test script

# Default format to bash if not specified
($ARGS.named.format // "bash") as $format |

# Validate schema has required fields
if (.name and .examples) | not then
  error("Schema must have 'name' and 'examples' fields")
else
  # Get transformation name first, before entering examples context
  .name as $transform_name |

  # Generate test cases from examples
  .examples | to_entries | map(
    {
      test_number: (.key + 1),
      description: .value.description,
      input: .value.input,
      args: (.value.args // {}),
      expected: .value.output
    }
  ) as $test_cases |

  # Output based on format
  if $format == "bash" then
    # Generate bash test script
    ([
      "#!/usr/bin/env bash",
      "set -euo pipefail",
      "",
      "# Test \($transform_name) transformation",
      "",
      "SCRIPT_DIR=\"$(cd \"$(dirname \"${BASH_SOURCE[0]}\")\" && pwd)\"",
      "TRANSFORM=\"$SCRIPT_DIR/transform.jq\"",
      "",
      "echo \"Testing \($transform_name) transformation...\"",
      ""
    ] +
    (
      $test_cases | map(
        # Build argument string for jq command
        (.args | to_entries | map("--arg \(.key) \"\(.value | tostring)\"") | join(" ")) as $arg_string |

        # Determine if output needs -c flag (for objects/arrays)
        (if (.expected | type) == "object" or (.expected | type) == "array" then "-c " else "" end) as $compact_flag |

        # Format expected value for bash comparison
        (.expected | if type == "string" then tojson else tostring end) as $expected_str |

        [
          "# Test \(.test_number): \(.description)",
          "echo -n \"Test \(.test_number): \(.description)... \"",
          "result=$(jq \($compact_flag)-f \"$TRANSFORM\" \($arg_string) <<'EOF'",
          (.input | tojson),
          "EOF",
          ")",
          "expected='\($expected_str)'",
          "if [[ \"$result\" == \"$expected\" ]]; then",
          "    echo \"PASS\"",
          "else",
          "    echo \"FAIL\"",
          "    echo \"  Expected: $expected\"",
          "    echo \"  Got: $result\"",
          "    exit 1",
          "fi",
          ""
        ]
      ) | flatten
    ) +
    [
      "echo \"All \($transform_name) tests passed!\""
    ]) | join("\n")
  else
    # Output as JSON array of test cases
    $test_cases
  end
end
