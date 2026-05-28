# MD5 Validation for Refactors

When refactoring existing pipelines or logic that produce output files, compare MD5 checksums with reference files before claiming parity.

## Example
```bash
md5sum path/to/reference_output.ext > reference.md5
md5sum path/to/new_output.ext > new.md5
diff -u reference.md5 new.md5
```

## Multi-file outputs
```bash
md5sum path/to/new_outputs/* > new.md5
md5sum path/to/reference_outputs/* > reference.md5
diff -u reference.md5 new.md5
```

If checksums differ, inspect the output differences and report the mismatch.
