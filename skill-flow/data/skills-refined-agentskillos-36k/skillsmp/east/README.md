# East

**East** is a statically typed, expression-based programming language embedded in TypeScript. Designed for the [Elara](https://elaraai.com/) platform, East enables you to write portable logic once and execute it across multiple environments (JavaScript, Julia, Python, and more), leveraging each language's native performance characteristics and ecosystem.

## Motivation

Delivering a complete business solution requires a wide range of technologies and activities: data integrations, mathematical optimization, machine learning, simulation, user interfaces, authentication & authorization, hosting, managing data consistency, auditing, etc.
Multiple programming environments are required to solve any given business problem - for example you may use JavaScript for web front ends and python for training and evaluating machine learning models.

East is designed to make it easy to fuse different technologies together by focussing on a simple yet powerful structural type system which makes all the bolierplate and plumbing work disappear, letting you spend more time solving real-world problems.
East is intentionally a simple language that is fast to learn and straightforward to implement in new runtimes.

## Features

- **🔒 Static Typing**: All types declared explicitly for speed and correctness
- **🎯 Structural Typing**: Lightweight and easy to use
- **🚀 Portable IR**: Compile to JavaScript, with Julia and Python backends coming soon
- **🔐 Controlled Side Effects**: Secure execution with platform-defined effects
- **🤖 LLM Friendly**: Designed for code generation with clear, composable TypeScript API & MCP integration
- **📦 Minimal Dependencies**: Single runtime dependency (sorted-btree for efficient collections)
- **🛡️ Total Ordering**: All types (even floats with NaN) have defined comparisons
- **🔄 Serializable**: All data can be serialized, functions can be transmitted as IR

## Development status

Note that at this stage of development, East does not have a concrete syntax.
Code is created through a TypeScript fluent interface.
Otherwise, East is quite usable and works end-to-end with multiple backend implementations (including a natively compiled one).
The East language is not considered "stable", and the implementation here may undergo breaking changes.

## Quick Start

### Installation

```bash
npm install @elaraai/east
```

### Basic Example


```typescript
import { East, IntegerType, ArrayType, StructType, StringType, DictType, NullType } from "@elaraai/east";

// Platform function for logging
const log = East.platform("log", [StringType], NullType);

const platform = [
    log.implement(console.log),
];

// Define sale data type
const SaleType = StructType({
    product: StringType,
    quantity: IntegerType,
    price: IntegerType
});

// Calculate revenue per product from sales data
const calculateRevenue = East.function(
    [ArrayType(SaleType)],
    DictType(StringType, IntegerType),
    ($, sales) => {
        // Group sales by product and sum revenue (quantity × price)
        const revenueByProduct = sales.groupSum(
            // Group by product name
            ($, sale) => sale.product,
            // Sum quantity × price    
            ($, sale) => sale.quantity.multiply(sale.price)
        );

        // Log revenue for each product
        $(log(East.str`Total Revenue: ${East.Integer.printCurrency(revenueByProduct.sum())}`));

        $.return(revenueByProduct);
    }
);

// Compile and execute
const compiled = East.compile(calculateRevenue, platform);

const sales = [
    { product: "Widget", quantity: 10n, price: 50n },
    { product: "Gadget", quantity: 5n, price: 100n },
    { product: "Widget", quantity: 3n, price: 50n }
];

compiled(sales);
// Total Revenue: $1,150
```

## Type System

East supports a rich type system optimized for business logic and data processing:

| Type | ValueTypeOf<Type> | Mutability | Description |
|------|-----------------|------------|-------------|
| **Primitive Types** | | | |
| `NullType` | `null` | Immutable | Unit type (single value) |
| `BooleanType` | `boolean` | Immutable | True or false |
| `IntegerType` | `bigint` | Immutable | 64-bit signed integers |
| `FloatType` | `number` | Immutable | IEEE 754 double-precision |
| `StringType` | `string` | Immutable | UTF-8 text |
| `DateTimeType` | `Date` | Immutable | UTC timestamp with millisecond precision |
| `BlobType` | `Uint8Array` | Immutable | Binary data |
| **Mutable Collections** | | | |
| `ArrayType<T>` | `ValueTypeOf<T>[]` | **Mutable** | Ordered collection |
| `SetType<K>` | `Set<ValueTypeOf<K>>` | **Mutable** | Sorted set |
| `DictType<K, V>` | `Map<ValueTypeOf<K>, ValueTypeOf<V>>` | **Mutable** | Sorted dictionary |
| `RefType<T>` | `ref<ValueTypeOf<T>>` | **Mutable** | Refcell, mutable box |
| **Compound types** | | | |
| `StructType<Fields>` | `{...}` | Immutable | Product type (records) |
| `VariantType<Cases>` | `variant` | Immutable | Sum type (tagged unions) |
| `RecursiveType<T>` | `ValueTypeOf<T>` | Immutable | Recursive references for trees, DAGs, and circular structures |
| **Function Type** | | | |
| `FunctionType<I, O>` | Function | Immutable | First-class functions/closures |
| `AsyncFunctionType<I, O>` | Function returning `Promise` | Immutable | Asynchronous functions/closures |

## Documentation

- **[SKILL.md](SKILL.md)** - Comprehensive guide with API and example reference
- **[LICENSE.md](LICENSE.md)** - Dual licensing information (AGPL-3.0 / Commercial)
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute to East
- **[CLA.md](CLA.md)** - Contributor License Agreement

## Key Concepts

### Platform Functions

East code runs in a controlled environment. You define **platform functions** that your East code can call:

```typescript
// Define platform function helper
const log = East.platform("log", [StringType], NullType);
const readFile = East.platform("readFile", [StringType], StringType);

// Provide implementations
const platform = {
    log: (msg: string) => console.log(msg),
    readFile: (path: string) => fs.readFileSync(path, 'utf-8')
};

// Compile with platform
const compiled = East.compile(myFunction, platform);
```

East also supports `asyncPlatform` functions (which may be called by `AsyncFunctionType` user-defined functions), inserting `await` automatically as required.
In the above, `readFile` could have be implented using `fs.promises.readFile` to take advantage of concurrency.

### Fluent Interface

Build expressions using chainable methods:

```typescript
const myFunction = East.function([IntegerType], IntegerType, ($, x) => {
    // Arithmetic
    const result = x.add(10n).multiply(2n).divide(3n);

    // Collections
    const arr = $.let([1n, 2n, 3n]);
    const doubled = arr.map(($, x, i) => x.multiply(2n));
    const sum = doubled.sum();

    $.return(sum);
});
```

### Serialization

All East data can be written and read in any of the following formats:

 * East text format (a JSON-like format designed for the East type system)
 * A binary East format called "beast" (compact, self-describing, streaming)
 * JSON (with a canonical encoding for each East type)

Note that mutable aliasing _is_ preserved through serialization/deserialization.

Function and closure values are not directly serializable (at least yet), but function definitions can be serialized as IR and transmitted across environments to compile and run on the other side:

```typescript
// Convert to IR
const ir = myFunction.toIR();

// Serialize to JSON (handles bigints, NaN, Infinity correctly)
const jsonData = ir.toJSON();
const jsonString = JSON.stringify(jsonData);

// Send over network, save to file, etc.
// ...

// Deserialize and compile
const receivedData = JSON.parse(jsonString);
const receivedIR = EastIR.fromJSON(receivedData);
const compiled = receivedIR.compile(platform);
```

## Examples

See the [USAGE.md](./USAGE.md) for more.

## Development

### Building

```bash
npm run build       # Compile TypeScript to JavaScript
npm run test        # Run test suite (requires build first)
npm run lint        # Check code quality with ESLint
npm run example     # Run the basic example
```

### Testing

East has a comprehensive test suite with tests covering:

- Type system operations
- Serialization formats (BEAST v1/v2, JSON, EAST text format)
- Collections and functional operations
- Error handling and edge cases

Notably, these tests are hosted in East and allow one to validate the correctness of a new runtime with ease (effectively acting as a compliance suite).

### Release Process

East uses automated releases via GitHub Actions. The process differs for stable and beta releases:

#### Stable Releases

For stable releases (published to npm with `latest` tag):

```bash
npm run release:patch    # 0.0.1 → 0.0.2
npm run release:minor    # 0.0.1 → 0.1.0
npm run release:major    # 0.0.1 → 1.0.0
```

These commands will:
1. Bump the version in `package.json`
2. Create a git commit with message `chore: bump version to X.Y.Z`
3. Create a git tag `vX.Y.Z`
4. Push the commit and tag to GitHub
5. GitHub Actions automatically builds, tests, and publishes to npm with `latest` tag

#### Beta Releases

For beta/prerelease versions (published to npm with `beta` tag):

```bash
npm run release:prepatch      # 0.0.1 → 0.0.2-beta.0
npm run release:preminor      # 0.0.1 → 0.1.0-beta.0
npm run release:premajor      # 0.0.1 → 1.0.0-beta.0
npm run release:prerelease    # 0.0.1-beta.0 → 0.0.1-beta.1
```

Beta releases follow the same automated process but are published to npm with the `beta` tag.

#### Manual Version Bumping (Dry Run)

To update the version without committing or tagging:

```bash
npm run version:patch:dry
npm run version:minor:dry
npm run version:major:dry
npm run version:prepatch:dry
npm run version:preminor:dry
npm run version:premajor:dry
npm run version:prerelease:dry
```

#### Requirements

- **Automated Publishing**: Requires `NPM_TOKEN` secret configured in GitHub repository settings
- **Pre-publish Checks**: All tests and linting must pass before publishing (enforced by `prepublishOnly` hook)
- **Node Version**: Requires Node.js ≥22.0.0

## License

This project is dual-licensed:

- **Open Source**: [AGPL-3.0](LICENSE.md) - Free for open source use with source disclosure requirements
- **Commercial**: Available for proprietary use - contact support@elara.ai

See [LICENSE.md](LICENSE.md) for full details.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

**Note**: Contributors must sign our [CLA](CLA.md) before we can accept pull requests. This allows us to offer commercial licenses while keeping the project open source.

### Ecosystem

- **[East Node](https://github.com/elaraai/east-node)**: Node.js platform functions for I/O, databases, and system operations. Connect East programs to filesystems, SQL/NoSQL databases, cloud storage, and network services.
  - [@elaraai/east-node-std](https://www.npmjs.com/package/@elaraai/east-node-std): Filesystem, console, HTTP fetch, crypto, random distributions, timestamps
  - [@elaraai/east-node-io](https://www.npmjs.com/package/@elaraai/east-node-io): SQLite, PostgreSQL, MySQL, MongoDB, S3, FTP, SFTP
  - [@elaraai/east-node-cli](https://www.npmjs.com/package/@elaraai/east-node-cli): CLI for running East IR programs in Node.js

- **[East Python](https://github.com/elaraai/east-py)**: Python runtime and platform functions for data science and machine learning. Execute East programs with access to optimization solvers, gradient boosting, neural networks, and model explainability.
  - [@elaraai/east-py-datascience](https://www.npmjs.com/package/@elaraai/east-py-datascience): TypeScript types for optimization, gradient boosting, neural networks, explainability

- **[East UI](https://github.com/elaraai/east-ui)**: East types and expressions for building dashboards and interactive layouts. Define UIs as data structures that render consistently across React, web, and other environments.
  - [@elaraai/east-ui](https://www.npmjs.com/package/@elaraai/east-ui): 50+ typed UI components for layouts, forms, charts, tables, dialogs
  - [@elaraai/east-ui-components](https://www.npmjs.com/package/@elaraai/east-ui-components): React renderer with Chakra UI styling

- **[e3 - East Execution Engine](https://github.com/elaraai/e3)**: Durable execution engine for running East pipelines at scale. Features Git-like content-addressable storage, automatic memoization, task queuing, and real-time monitoring.
  - [@elaraai/e3](https://www.npmjs.com/package/@elaraai/e3): SDK for authoring e3 packages with typed tasks and pipelines
  - [@elaraai/e3-core](https://www.npmjs.com/package/@elaraai/e3-core): Git-like object store, task queue, result caching
  - [@elaraai/e3-types](https://www.npmjs.com/package/@elaraai/e3-types): Shared type definitions for e3 packages
  - [@elaraai/e3-cli](https://www.npmjs.com/package/@elaraai/e3-cli): `e3 init`, `e3 run`, `e3 logs` commands for managing and monitoring tasks
  - [@elaraai/e3-api-client](https://www.npmjs.com/package/@elaraai/e3-api-client): HTTP client for remote e3 servers
  - [@elaraai/e3-api-server](https://www.npmjs.com/package/@elaraai/e3-api-server): REST API server for e3 repositories

## Links

- **Website**: [https://elaraai.com/](https://elaraai.com/)
- **Repository**: [https://github.com/elaraai/east](https://github.com/elaraai/east)
- **Issues**: [https://github.com/elaraai/east/issues](https://github.com/elaraai/east/issues)
- **Email**: support@elara.ai

## About Elara

East is developed by [Elara AI Pty Ltd](https://elaraai.com/), an AI-powered platform that creates economic digital twins of businesses that optimize performance. Elara combines business objectives, decisions and data to help organizations make data-driven decisions across operations, purchasing, sales and customer engagement, and project and investment planning. East powers the computational layer of Elara solutions, enabling the expression of complex business logic and data in a simple, type-safe and portable language.

---

*Developed by [Elara AI Pty Ltd](https://elaraai.com/)*
