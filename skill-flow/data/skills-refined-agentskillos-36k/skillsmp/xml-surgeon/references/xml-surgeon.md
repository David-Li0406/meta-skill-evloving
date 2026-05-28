# XML Surgeon

## XPath quick use
- Select by tag: `//record`
- Filter attributes: `//field[@name='arch']`
- Match by contains: `//*[contains(@name,'foo')]`
- Position: `//page[1]`, `//group[last()]`
- Namespaces: `--ns prefix=uri` and use `//prefix:tag`

## Minimal-diff guidance
- Use `--diff` first; only `--in-place` after review.
- `set-attr`, `del-attr`, `set-text` are surgical (no reformat).
- `insert`, `replace`, `delete` reserialize XML and require `--reformat-ok`.
- Insert/replace: set `--indent` if you see indentation drift.

## Semantic reads
- `show` outputs the selected subtree (`--inner` for children/text only).
- `children` summarizes direct child tags; add `--list` for a full list.
- `select` gives match counts and sourcelines for navigation.
- `outline` prints a shallow tree view for quick structure scans.
- `context` prints file lines around each matched element.

## Large / nested XML
- Use `--huge` for very large trees.
- `--recover` only for damaged XML (may drop nodes).

## Odoo-ish patterns (optional)
- Views often under `//record[@model='ir.ui.view']`.
- The view arch is typically inside `//field[@name='arch']`.
- XPath can target nested view nodes directly (they are real XML elements).
