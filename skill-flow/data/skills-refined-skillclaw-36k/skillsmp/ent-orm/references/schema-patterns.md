# Ent Schema Patterns

## Schema Definition

```go
// ent/schema/user.go
package schema

import (
    "time"
    "entgo.io/ent"
    "entgo.io/ent/schema/field"
    "entgo.io/ent/schema/edge"
    "entgo.io/ent/schema/index"
)

type User struct {
    ent.Schema
}

func (User) Fields() []ent.Field {
    return []ent.Field{
        field.String("name").
            NotEmpty().
            MaxLen(100),
        field.String("email").
            Unique(),
        field.Int("age").
            Positive().
            Optional(),
        field.Bool("active").
            Default(true),
        field.Enum("role").
            Values("admin", "user", "guest").
            Default("user"),
        field.Time("created_at").
            Default(time.Now).
            Immutable(),
        field.Time("updated_at").
            Default(time.Now).
            UpdateDefault(time.Now),
    }
}

func (User) Edges() []ent.Edge {
    return []ent.Edge{
        // One-to-many: User has many Posts
        edge.To("posts", Post.Type),
        // Many-to-many: User has many Groups
        edge.To("groups", Group.Type),
        // Inverse edge: User belongs to a Company
        edge.From("company", Company.Type).
            Ref("employees").
            Unique(),
    }
}

func (User) Indexes() []ent.Index {
    return []ent.Index{
        index.Fields("email").Unique(),
        index.Fields("name", "created_at"),
    }
}
```

## Edge Definitions

```go
// Post schema
type Post struct {
    ent.Schema
}

func (Post) Fields() []ent.Field {
    return []ent.Field{
        field.String("title"),
        field.Text("content"),
    }
}

func (Post) Edges() []ent.Edge {
    return []ent.Edge{
        // Inverse of User.posts
        edge.From("author", User.Type).
            Ref("posts").
            Unique().
            Required(),
        // Self-referential: parent comment
        edge.To("children", Post.Type).
            From("parent").
            Unique(),
    }
}
```

## CRUD Operations

```go
import "myapp/ent"

func main() {
    client, _ := ent.Open("postgres", "...")
    defer client.Close()
    ctx := context.Background()

    // Create
    user, err := client.User.
        Create().
        SetName("John").
        SetEmail("john@example.com").
        SetAge(30).
        Save(ctx)

    // Create with edges
    post, _ := client.Post.
        Create().
        SetTitle("Hello").
        SetContent("World").
        SetAuthor(user).
        Save(ctx)

    // Read
    user, _ = client.User.Get(ctx, 1)
    user, _ = client.User.
        Query().
        Where(user.EmailEQ("john@example.com")).
        Only(ctx)

    // Update
    user, _ = client.User.
        UpdateOne(user).
        SetAge(31).
        Save(ctx)

    // Bulk update
    affected, _ := client.User.
        Update().
        Where(user.AgeGT(18)).
        SetActive(true).
        Save(ctx)

    // Delete
    client.User.DeleteOne(user).Exec(ctx)
}
```

## Queries

```go
// Eager loading edges
users, _ := client.User.
    Query().
    WithPosts().
    WithGroups().
    All(ctx)

for _, u := range users {
    for _, p := range u.Edges.Posts {
        fmt.Println(p.Title)
    }
}

// Complex queries
users, _ := client.User.
    Query().
    Where(
        user.And(
            user.AgeGTE(18),
            user.ActiveEQ(true),
        ),
    ).
    Order(ent.Desc(user.FieldCreatedAt)).
    Limit(10).
    Offset(0).
    All(ctx)

// Aggregations
count, _ := client.User.
    Query().
    Where(user.ActiveEQ(true)).
    Count(ctx)

// Select specific fields
var v []struct {
    Name  string `json:"name"`
    Email string `json:"email"`
}
client.User.
    Query().
    Select(user.FieldName, user.FieldEmail).
    Scan(ctx, &v)
```

## Hooks

```go
func (User) Hooks() []ent.Hook {
    return []ent.Hook{
        // Before create/update
        hook.On(
            func(next ent.Mutator) ent.Mutator {
                return hook.UserFunc(func(ctx context.Context, m *ent.UserMutation) (ent.Value, error) {
                    // Validate or modify
                    if name, ok := m.Name(); ok && name == "" {
                        return nil, errors.New("name cannot be empty")
                    }
                    return next.Mutate(ctx, m)
                })
            },
            ent.OpCreate|ent.OpUpdate,
        ),
    }
}
```

## Transactions

```go
tx, err := client.Tx(ctx)
if err != nil {
    return err
}

user, err := tx.User.Create().
    SetName("John").
    Save(ctx)
if err != nil {
    tx.Rollback()
    return err
}

_, err = tx.Post.Create().
    SetTitle("First Post").
    SetAuthor(user).
    Save(ctx)
if err != nil {
    tx.Rollback()
    return err
}

return tx.Commit()
```

## Generate Commands

```bash
# Initialize ent
go run -mod=mod entgo.io/ent/cmd/ent new User

# Generate code
go generate ./ent

# With features
go run -mod=mod entgo.io/ent/cmd/ent generate --feature sql/upsert ./ent/schema
```
