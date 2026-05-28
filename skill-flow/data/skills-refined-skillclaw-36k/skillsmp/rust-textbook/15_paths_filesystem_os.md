# 15 — Paths, Filesystems, OS Boundaries (Portability and TOCTOU)

[CONTRACT: CTR-1501] Paths Are Not UTF-8 Strings.
- REJECT IF: APIs force `Path` through UTF-8 without a contract requirement.
- ENFORCE BY: `Path`/`PathBuf` and `OsStr`/`OsString` at boundaries; convert to UTF-8 only where explicitly required.
[PROVENANCE] std path and OS string types exist to represent platform-native encodings.

[HAZARD: RSK-1501] Canonicalization as a Security Decision (TOCTOU).
- TRIGGER: `canonicalize()` used for access control, sandboxing, or path validation.
- FAILURE MODE: symlink races; path meaning changes between check and use.
- REJECT IF: canonicalization is used as a security primitive without an open-by-handle strategy.
- ENFORCE BY: avoid check-then-open; use OS-specific safe-open patterns; treat symlink traversal explicitly.
[PROVENANCE] Filesystem operations are inherently racy; std `canonicalize` resolves symlinks and performs I/O.
[VERIFICATION] Integration tests with symlink race harnesses where feasible; platform-specific tests for safe-open behavior.

[CONTRACT: CTR-1503] Symlink Awareness and Rejection.
- REJECT IF: security-sensitive operations follow symlinks without an explicit policy.
- ENFORCE BY:
  - use `symlink_metadata()` to detect symlinks before access.
  - reject symlinks at the boundary for workspace-confined paths.
[PROVENANCE] APM2 Security Policy; CTR-2609.

```rust
// Pattern: Reject if symlink
pub fn reject_if_any_symlink(path: &Path) -> io::Result<()> {
    let metadata = std::fs::symlink_metadata(path)?;
    if metadata.file_type().is_symlink() {
        return Err(io::Error::new(io::ErrorKind::PermissionDenied, "symlink disallowed"));
    }
    Ok(())
}
```

[CONTRACT: CTR-1504] Path Sanitization and Traversal Rejection.
- REJECT IF: untrusted paths are used without sanitizing `..` components or absolute path prefixes.
- ENFORCE BY:
  - iterate over `components()` and reject `ParentDir`, `RootDir`, or `Prefix`.
  - confine paths to a known root.
[PROVENANCE] APM2 Security Policy; CTR-2609.

```rust
// Pattern: Path Sanitization
pub fn sanitize_relative_path(p: &Path) -> Result<PathBuf, Error> {
    if p.is_absolute() { return Err(Error::NotRelative); }
    let mut out = PathBuf::new();
    for c in p.components() {
        match c {
            Component::Normal(seg) => out.push(seg),
            Component::CurDir => {}
            Component::ParentDir | Component::RootDir | Component::Prefix(_) => {
                return Err(Error::ForbiddenComponent)
            }
        }
    }
    Ok(out)
}
```

[CONTRACT: CTR-1502] Atomic Write Protocol for State Files.
- REJECT IF: files are written in-place when partial writes can corrupt state.
- ENFORCE BY: write-to-temp, fsync (when durability required), atomic rename, permission/ownership management.
[PROVENANCE] std filesystem APIs provide rename; atomicity is platform-dependent and must be treated as a contract.

[INVARIANT: INV-1501] Resource Lifetime Discipline.
- REJECT IF: OS handles can leak across error paths or panics.
- ENFORCE BY: RAII; explicit scope boundaries; avoid hidden global handles.
[PROVENANCE] Drop closes resources; drop order is defined by scopes.
[VERIFICATION] Tests that force early returns and panics; leak detection tooling where available.

## References (Normative Anchors)

- std path module: https://doc.rust-lang.org/std/path/
- std fs module: https://doc.rust-lang.org/std/fs/
