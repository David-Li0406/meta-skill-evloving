---
name: query-data
description: Expert guide to the auto-generated GraphQL API (Queries, Mutations, Aggregations).
---
# Query Data Skill

## 1. Naming Conventions
The Platform auto-generates GraphQL fields from your SCL schema.
*   **Namespace:** `app__` prefix (snake_case).
*   **Tables:** `app__plural` (List), `app__singular` (By ID).
*   **Mutations:** `insert_...`, `update_...`, `delete_...`.

Example: App `com.acme.crm` (`com_acme_crm`), Table `user` (`users`).
*   Query List: `com_acme_crm__users`
*   Query Single: `com_acme_crm__user`

## 2. Reading Data (Query)

### Basic List
```graphql
query ListUsers {
  users: com_acme_crm__users(
    limit: 10
    offset: 0
    order_by: { created_at: desc }
  ) {
    id
    email
    # Nested relationship
    orders {
      id
      total
    }
  }
}
```

### Filtering (`where`)
| Operator | Logic | Example |
| :--- | :--- | :--- |
| `_eq`, `_neq` | Equals / Not Equals | `{ status: { _eq: "active" } }` |
| `_gt`, `_lt` | Greater / Less Than | `{ count: { _gt: 5 } }` |
| `_in`, `_nin` | In List | `{ id: { _in: ["A", "B"] } }` |
| `_is_null` | Is Null | `{ notes: { _is_null: true } }` |
| `_and`, `_or` | Logic Groups | `{ _or: [ { a: ... }, { b: ... } ] }` |

### Aggregations (Stats)
Fetch counts, sums, averages.
*   **`_agg` Suffix:** Use `table_name_agg`.
*   **`aggregate`:** Holds the stats.
*   **`nodes`:** Holds the actual records (optional).

```graphql
query UserStats {
  com_acme_crm__users_agg(where: { status: { _eq: "active" } }) {
    aggregate {
      count
      sum { lifetime_value }
      avg { age }
    }
  }
}
```

## 3. Modifying Data (Mutation)

### Insert
```graphql
mutation NewUser($data: JSON!) {
  # returns the created object
  insert_com_acme_crm__user(object: $data) {
    id
  }
}
```

### Update (Patch)
```graphql
mutation MakeActive($id: ID!) {
  update_com_acme_crm__user(
    id: $id
    _set: { status: "active", updated_at: "now()" }
  ) {
    id
    status
  }
}
```

### Delete
```graphql
mutation RemoveUser($id: ID!) {
  delete_com_acme_crm__user(id: $id) {
    id
  }
}
```

## 4. Advanced Querying (Aggregation + Nodes)

### Mixed Pagination
Get the TOTAL count of matches (aggregate) but only fetch the FIRST PAGE of actual data (nodes).

```graphql
query SearchAndPaginate {
  com_acme_crm__users_agg(
    where: { status: { _eq: "active" } }
    order_by: { created_at: desc }
    limit: 20  # Applies to 'nodes'
    offset: 0  # Applies to 'nodes'
  ) {
    # 1. Total count matching the filter (ignoring limit!)
    aggregate {
      count
    }
    # 2. The actual page of data (respected limit)
    nodes {
      id
      email
    }
  }
}
```

### Nested Aggregation
Calculate stats for related records (e.g., Average Order Value per User).

```graphql
query UserStats {
  users: com_acme_crm__users {
    email
    # Aggregate on relationship
    orders_agg {
      aggregate {
        count
        sum { total }
      }
    }
  }
}
```

## 5. Introspection
When in doubt, query the schema itself to discover available types and fields.

```graphql
query Introspection {
  __schema {
    types { name kind }
  }
}
```
