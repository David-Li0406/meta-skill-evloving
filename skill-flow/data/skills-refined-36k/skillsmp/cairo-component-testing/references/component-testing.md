# Component Testing Reference

Source: https://www.starknet.io/cairo-book/ch103-02-03-testing-components.html

## Testing approach
- Create a mock contract that embeds the component using `component!`.
- Add component storage with `substorage(v0)` and include component events in the Event enum.
- Expose component functions with an impl alias marked `#[abi(embed_v0)]`.
- Use the component dispatcher in tests to call component functions.
