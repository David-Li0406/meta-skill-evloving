# Component Dependencies Reference

Source: https://www.starknet.io/cairo-book/ch103-02-02-component-dependencies.html

## Dependency model
- Components cannot embed other components directly.
- Dependencies are expressed via trait bounds on the host contract state.

## Access helpers
- Use `get_dep_component!` and `get_dep_component_mut!` to access dependencies via the host.
- The host contract must embed all required components in storage and events.
