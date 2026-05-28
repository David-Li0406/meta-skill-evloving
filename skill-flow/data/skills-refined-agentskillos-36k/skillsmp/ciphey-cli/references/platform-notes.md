# Platform notes

## macOS (Apple Silicon / arm64)

- The PyPI release (`ciphey==5.14.0`) depends on `cipheycore` wheels that do not target `macos arm64`.
- Prefer the Docker runner (`remnux/ciphey`) on Apple Silicon.

## macOS (x86_64 / Intel)

- `cipheycore` wheels exist for `macosx_10_15_x86_64`, but may still be sensitive to the Python distribution used.
- If the uv runner fails, use the Docker runner.

