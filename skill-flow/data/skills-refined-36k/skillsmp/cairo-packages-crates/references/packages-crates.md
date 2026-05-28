# Cairo Packages and Crates Reference

Source: https://www.starknet.io/cairo-book/ch07-01-packages-and-crates.html

## Definitions
- A package is a Scarb project described by a `Scarb.toml` manifest.
- A crate is a compilation unit; packages can contain one or more crates.

## Defaults
- `scarb new <name>` creates a package with a default library crate.
- The crate root for a library is `src/lib.cairo`.

## Multiple crates
- Additional crates are declared in `Scarb.toml`.
- Each crate has its own crate root file.
