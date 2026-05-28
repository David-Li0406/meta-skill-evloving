# Contract Classes and Instances Reference

Source: https://www.starknet.io/cairo-book/ch100-01-contracts-classes-and-instances.html

## Core concepts
- A contract class is the compiled code (Sierra/CASM) plus ABI and entry point metadata.
- A contract instance is a deployed address with its own storage, tied to a class hash.
- Class hashes uniquely identify compiled classes; they are derived from the program and ABI.

## Declare vs deploy
- Declaring registers a class on-chain and yields a class hash.
- Deploying creates an instance with an address and initializes storage via the constructor.

## Contract address
- The contract address is derived from the class hash, deployer address, constructor calldata, and a deployment salt.

## Upgrades
- Code is immutable once deployed; upgrades typically use proxy contracts that delegate to new classes.
