# Components Reference

Source: https://www.starknet.io/cairo-book/ch103-02-00-composability-and-components.html

## Core idea
- Components are modules with storage, events, and functions that can be embedded in contracts.
- Components are not deployable; they must be embedded in a contract.

## Defining components
- Mark the module with `#[starknet::component]`.
- Define component storage and event enum within the module.
- Define interface traits with `#[starknet::interface]`.
- Use `#[embeddable_as(Name)]` on impls to expose entry points.

## Embedding
- Use `component!` in the host contract to generate `HasComponent`.
- Add the component storage field with `substorage(v0)` in the contract storage.
- Embed component events into the contract Event enum.
- Use `#[abi(embed_v0)]` on impl aliases to expose component methods.
