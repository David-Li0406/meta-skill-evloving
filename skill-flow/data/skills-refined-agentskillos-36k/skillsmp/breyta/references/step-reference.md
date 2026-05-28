# Step reference
Condensed step families and common fields:

- `:http`: `:connection` or `:url`, `:path`, `:method`, `:query`, `:headers`, `:json`, `:body`, `:persist`, `:retry` (large bodies require `:persist`)
- `:llm`: `:connection`, `:model`, `:messages` or `:prompt`, `:template`, `:data`
- `:db`: `:connection`, `:query`, `:params`, `:template`, `:data`
- `:wait`: `:key`, `:notify`, `:timeout`
- `:function`: `:code` or `:ref`, `:input`

Detailed docs:
- `./steps/http.md`
- `./steps/llm.md`
- `./steps/db.md`
- `./steps/wait.md`
- `./steps/function.md`
- `./persist.md`
