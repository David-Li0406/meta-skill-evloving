# Smart Contract Testing Reference

Source: https://www.starknet.io/cairo-book/ch104-02-testing-smart-contracts.html

## Tools
- Starknet Foundry provides a testing framework for Cairo contracts.
- Tests typically declare and deploy contracts, then call via dispatchers.

## Patterns
- Use dispatchers to call entry points and check results.
- Use cheatcodes to modify caller address or block context.
- Use event spying to assert events emitted by contract calls.

## Helpers
- Some tests use `contract_state_for_testing` to test without deployment.
