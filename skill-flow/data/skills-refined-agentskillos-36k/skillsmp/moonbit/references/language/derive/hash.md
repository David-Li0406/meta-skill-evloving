### Deriving traits

#### Hash

`derive(Hash)` will generate a hash implementation for the type.
This will allow the type to be used in places that expects a `Hash` implementation,
for example `HashMap`s and `HashSet`s.

```moonbit
struct DeriveHash {
  x : Int
  y : String?
} derive(Hash, Eq, Show)

test "derive hash struct" {
  let hs = @hashset.new()
  hs.add(DeriveHash::{ x: 123, y: None })
  hs.add(DeriveHash::{ x: 123, y: None })
  assert_eq(hs.length(), 1)
  hs.add(DeriveHash::{ x: 123, y: Some("456") })
  assert_eq(hs.length(), 2)
}
```

