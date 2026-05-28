# DB step (`:db`)
Use for SQL queries against a database connection.

Core fields:

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `:connection` | keyword/string | Yes | Slot or connection id |
| `:query` | string | Yes (unless `:template`) | SQL string |
| `:params` | vector | No | Query params (positional) |
| `:template` | keyword | No | Template id |
| `:data` | map | No | Template inputs |

Notes:
- Prefer `:template` for long queries or shared SQL.

Example:

```clojure
;; In the flow definition:
;; :templates [{:id :user-by-id
;;              :type :sql
;;              :query "select id, email from users where id = :id"}]

(flow/step :db :get-user
           {:connection :db
            :template :user-by-id
            :data {:id user-id}})
```
