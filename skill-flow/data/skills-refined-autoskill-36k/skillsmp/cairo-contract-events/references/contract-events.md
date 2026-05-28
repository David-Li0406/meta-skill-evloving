# Contract Events Reference

Source: https://www.starknet.io/cairo-book/ch101-03-contract-events.html

## Defining events
- Contracts define an `Event` enum annotated with `#[event]` and `#[derive(starknet::Event)]`.
- Each variant can hold a struct or tuple carrying the event data.

## Emitting events
- Use `self.emit(Event::Variant(...))` in contract functions.

## Indexed fields
- Annotate event fields with `#[key]` to mark them as indexed topics.
