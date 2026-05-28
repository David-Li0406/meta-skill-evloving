# 14 — Unicode, UTF-8, Graphemes (Text Correctness and Security)

[INVARIANT: INV-1401] `str` Validity (UTF-8).
- REJECT IF: `&str` is constructed from bytes without proving UTF-8 validity.
- ENFORCE BY: `std::str::from_utf8` for validation; keep raw bytes as `&[u8]` until a UTF-8 contract is required.
[PROVENANCE] std docs: `str` is valid UTF-8 and library methods may assume validity.
[VERIFICATION] Fuzzers and property tests for UTF-8 boundary construction; Miri for unsafe `from_utf8_unchecked` boundaries.

[CONTRACT: CTR-1401] Text Unit Must Be Specified.
- Units: bytes (`u8`), Unicode scalar values (`char`), grapheme clusters (UAX #29), user-visible rendering (locale/font).
- REJECT IF: APIs use "character position" without defining the unit.
- ENFORCE BY: expose iterators (`bytes()`, `chars()`); provide explicit grapheme segmentation only when required by contract.
[PROVENANCE] std `str` operates over UTF-8 bytes; `char` is a Unicode scalar value.

[HAZARD: RSK-1401] Indexing/Slicing Panics and Unit Confusion.
- TRIGGER: `s[i]`, `&s[i..j]`, manual byte offsets interpreted as character indices.
- FAILURE MODE: panic-as-DoS; data corruption when offsets are misinterpreted.
- REJECT IF: string indexing/slicing is used without proving byte boundary correctness and a panic policy.
- ENFORCE BY: operate on bytes for protocol formats; use iterator-based traversal for character-aware logic.
[PROVENANCE] std docs: string indexing is not supported; slicing requires UTF-8 boundary alignment.

[CONTRACT: CTR-1402] Grapheme Cluster Semantics Require Explicit Policy.
- REJECT IF: user-visible text editing/cursor movement is implemented using `char` iteration without a grapheme policy.
- ENFORCE BY: UAX #29 segmentation when contract requires "what users perceive"; treat dependency choice as a governed decision.
[PROVENANCE] Unicode UAX #29 defines default grapheme cluster segmentation; std does not implement UAX #29.
[VERIFICATION] Corpus tests covering combining marks and emoji sequences.

[HAZARD: RSK-1402] Normalization and Confusables in Security-Relevant Comparisons.
- TRIGGER: identifier comparison, authz/authn checks, path-like semantics, key normalization.
- FAILURE MODE: confusable identifiers; multiple encodings of "same" visible string; case-folding drift.
- REJECT IF: security-relevant comparisons occur without an explicit normalization/case policy.
- ENFORCE BY: define normalization and case-folding policy; treat text as opaque bytes when Unicode semantics are not a requirement.
[PROVENANCE] Unicode normalization and confusables are security-relevant; correctness requires explicit policy.
[VERIFICATION] Test vectors for normalization and confusable sets relevant to the domain.

## References (Normative Anchors)

- std `str`: https://doc.rust-lang.org/std/primitive.str.html
- std `String`: https://doc.rust-lang.org/std/string/struct.String.html
- Unicode UAX #29: https://www.unicode.org/reports/tr29/
