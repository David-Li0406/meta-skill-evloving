---
name: review-migrated-code
description: Review migrated go source code
---

- Make sure structs don't hold *Base values either as fields or as collections. Its okay to use inclusion on them
    - Instead you should use an interface value

- Interfaces should be defined in terms of other interfaces. ie parameters and return types should be interfaces.

- Fields that takes the same amount of space (pointers, int, bool, struct values of same type) should be grouped together.
