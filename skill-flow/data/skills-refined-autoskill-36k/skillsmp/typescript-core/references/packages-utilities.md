# Packages – Utilities & Misc

This covers assorted utility libraries and our stance on them, beyond the core categories above.

## type-fest – TypeScript Type Utilities
`type-fest` is a collection of TypeScript type utilities such as `PartialDeep<T>`, `Opaque<Type, Token>` (for branded types), `Jsonify<T>`, `SetOptional<T, Keys>` etc. Improves devx, include as a dev dependency since it’s types only.

We should use `type-fest` for:
- Creating branded types for IDs (there’s `Opaque` or `Brand` type).
- Strict typing on JSON (the `JsonValue` type).
- Deep partial/required or filtering properties.
- Ensuring literal types via `LiteralUnion` or string transformations, etc.

**WARNING:** Sometimes the advanced types can be heavy on compile time. Don’t overuse to the point TS language server slows down.

## ts-pattern – Pattern Matching for TS - https://github.com/gvergnaud/ts-pattern
`ts-pattern` provides algebraic pattern matching for TS discriminated unions and other types, with exhaustive checking.

We should use `ts-pattern` when:
- We have a `Result` and want to pattern match `Ok`/`Err` instead of `if/else`.
- We have complex union types (e.g., different variants of a message or shape).
- It makes code more declarative. For instance, state machines or reducers can be nicely written with pattern matching.

Example:

  ```
  import { match, P } from 'ts-pattern';

  type Data =
    | { type: 'text'; content: string }
    | { type: 'img'; src: string };

  type Result =
    | { type: 'ok'; data: Data }
    | { type: 'error'; error: Error };

  const result: Result = ...;

  const html = match(result)
    .with({ type: 'error' }, () => <p>Oups! An error occured</p>)
    .with({ type: 'ok', data: { type: 'text' } }, (res) => <p>{res.data.content}</p>)
    .with({ type: 'ok', data: { type: 'img', src: P.select() } }, (src) => <img src={src} />)
    .exhaustive();
  ```


## Tailwind Variants – Utility for Tailwind CSS - https://www.tailwind-variants.org/docs/introduction
`tailwind-variants` is a library to create variant-based utility classes in Tailwind CSS, making it easier to manage conditional styles. Include it anytime we use Tailwind (basically every project with a Web based frontend, including Tauri apps)

Example:

  ```
  import { tv } from 'tailwind-variants';
 
  const button = tv({
    base: 'font-medium bg-blue-500 text-white rounded-full active:opacity-80',
    variants: {
      color: {
        primary: 'bg-blue-500 text-white',
        secondary: 'bg-purple-500 text-white'
      },
      size: {
        sm: 'text-sm',
        md: 'text-base',
        lg: 'px-4 py-3 text-lg'
      }
    },
    compoundVariants: [
      {
        size: ['sm', 'md'],
        class: 'px-3 py-1'
      }
    ],
    defaultVariants: {
      size: 'md',
      color: 'primary'
    }
  });
  
  return (
    <button className={button({ size: 'sm', color: 'secondary' })}>
      Click me
    </button>
  );
  ```

## es-toolkit – Modern Lodash Alternative - https://es-toolkit.dev/

`es-toolkit` is a utility library aiming to replace Lodash with faster, smaller implementations of common helpers. **Always** use `es-toolkit` in place of lodash.

We should:
- Replace any Lodash usage with `es-toolkit` equivalents.
- If a dev needs to do something like `debounce` or `deepClone`, reach for `es-toolkit` first.

## typeid-js – Type-safe Unique IDs - https://github.com/jetify-com/typeid-js
`typeid-js` implements TypeIDs – a format for unique IDs that include a type prefix and are k-sortable (based on time, like UUIDv7).

Using TypeIDs in our projects:
- It can replace using UUIDs for database primary keys or identifiers. Instead of a bare UUID string `"123e4567-e89b-12d3..."`, you have `"user_2x4y6..."`.
- **Type safety**: with their TS lib, we can create a `TypeID<'user'>` which is a branded string that ensures at compile time you don't mix IDs of different types.

We should ensure:
- Our DB fields can accommodate slightly longer strings (TypeID is 27 chars after prefix vs UUID 36 chars with hyphens, so length is fine).
- We have to update any client code that might assume ID format (but if it's all new dev, just standardize on this).

We will:
- Add `typeid-js` to back-end services where we generate IDs (like in a `createUser` function, use `TypeID` instead of `uuid`).
- Possibly store them as strings in DB (just treat as strings).
- On the client side, if using TypeScript, we could also leverage the `TypeID` type for better type checking.

Example:

  ```
  import { typeid } from 'typeid-js';
  const tid = typeid('prefix');
  ```

## Conclusion on Utilities

We prefer to use small, focused utilities over writing our own one-off implementations (which may be error-prone). However, we also avoid adding too many trivial dependencies:

- Many simple things can be done with modern JS (e.g., `Array.at(-1)` instead of Lodash `_.last`).
- For those that can’t, we use the above libraries.

Our choices lean toward well-maintained, modern, typed libraries (`type-fest`, `es-toolkit`, `ts-pattern`, etc.) and away from older or unmaintained ones.

By following these guidelines, we keep our codebase modern, reduce bugs, and ensure we’re not re-solving solved problems. Each addition to our toolkit is justified by clear benefits and checked for long-term viability, consistent with our dependency guidelines (see `dependencies.md`).