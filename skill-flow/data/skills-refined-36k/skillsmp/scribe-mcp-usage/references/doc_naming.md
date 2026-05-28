# Document Naming and Categories

`doc_name`:
- Unique document identifier and filename key.
- Used for registry keys and path resolution.

`doc_category`:
- Semantic classification only.
- Must not be used as a filename or registry key.

Registration rules:
- `create_doc` registers by default unless `metadata.register_doc=false`.
- Edit actions attempt auto-registration by `doc_name` when the resolved file exists.
- For non-standard `doc_name`, the fallback filename is `<DOC_NAME>.md` under the project's docs directory.
