# Components Under the Hood Reference

Source: https://www.starknet.io/cairo-book/ch103-02-01-under-the-hood.html

## Generated traits
- The `component!` macro generates a `HasComponent` trait for the host contract.
- `HasComponent` provides `get_component`, `get_component_mut`, `get_contract`, and `emit` helpers.

## ComponentState
- `ComponentState<TContractState>` wraps access to the host contract storage and events.
- Embeddable impls use `ComponentState` to call into the host contract safely.

## Embedding flow
- `#[starknet::embeddable]` and `#[embeddable_as]` define component entry points.
- The compiler generates a concrete impl in the contract that delegates to the component.
