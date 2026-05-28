---
name: sync-test-binary
description: Update test binaries (test_stream_generator.rs) to match the latest architecture from main.rs, ensuring they use the same caching, rendering, and pagination patterns. Use when test binaries need to be synchronized with production code.
allowed-tools: Read, Edit, Bash, Grep
---

# Sync Test Binary Architecture

Synchronize test binaries with the latest architecture patterns from `main.rs`.

## Step 1: Extract Architecture Patterns from main.rs

Read `src/main.rs` and identify current patterns:

1. **Cache creation** - Look for DataCache::new() before page loop
2. **Cache conditions** - Check `page_values.len() > 1` logic
3. **PlotRenderer creation** - Look for new_with_cache() usage
4. **Cache cleanup** - Find cache.clear() after page loop

## Step 2: Identify Test Binary

Find test binary at `src/bin/test_stream_generator.rs`

## Step 3: Compare and Find Gaps

Compare test binary with main.rs patterns:
- Missing DataCache creation?
- Still using PlotRenderer::new() instead of new_with_cache()?
- Missing cache cleanup?

## Step 4: Apply Cache Creation Pattern

**Location**: Before the page loop (after page_values extraction)

Add this code:
```rust
// Create shared disk cache for all pages (only if multiple pages)
use ggrs_core::stream::DataCache;
let cache = if page_values.len() > 1 {
    let cache = DataCache::new(&workflow_id, &step_id)?;
    println!("  Created disk cache at /tmp/ggrs_cache_{}_{}/", workflow_id, step_id);
    Some(cache)
} else {
    println!("  Single page - cache disabled");
    None
};
```

## Step 5: Update PlotRenderer Creation

**Location**: Where PlotRenderer::new() is called

Replace:
```rust
let renderer = PlotRenderer::new(&plot_gen, plot_width as u32, plot_height as u32);
```

With:
```rust
// Create PlotRenderer with cache (if enabled)
let renderer = if let Some(ref cache_ref) = cache {
    PlotRenderer::new_with_cache(&plot_gen, plot_width as u32, plot_height as u32, cache_ref.clone())
} else {
    PlotRenderer::new(&plot_gen, plot_width as u32, plot_height as u32)
};
```

## Step 6: Add Cache Cleanup

**Location**: After the page loop ends

Add this code:
```rust
// Clean up cache directory after all pages are rendered
if let Some(ref cache_ref) = cache {
    println!("  Cleaning up disk cache...");
    cache_ref.clear()?;
}
```

## Step 7: Verify Compilation

Build the test binary:
```bash
cargo build --bin test_stream_generator
```

If errors occur, fix:
- Missing imports (add `use ggrs_core::stream::DataCache;`)
- Variable naming mismatches
- Scope issues with cache variable

## Step 8: Report Changes

Provide summary:
- File modified
- Line numbers where patterns were added
- Compilation status
- What to test next

## Edge Cases

- If test binary has no pagination, skip cache entirely
- If workflow_id/step_id missing, they're already extracted from environment in test binary
- If cache logic already exists, verify it exactly matches main.rs
