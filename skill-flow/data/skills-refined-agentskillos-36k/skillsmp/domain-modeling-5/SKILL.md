---
name: domain-modeling
description: Use this when asked to model a metadomain, domain, or think about domain boundaries, or construct schema to serve customer needs.
---

## Meaning of "metadomain"

There exist two metadomains: **internal** and a **external**.

## External Domain

The external domain comprises the means by which the system's users interact with it.

Software exists to serve the needs of its users, and the **external domain** is where those needs are first surfaced.

Users make requests to the internal domain (e.g. via an API) and expect the system to produce expected side effects and return meaningful data.

A user can typically describe their needs in broad strokes; it is our job to translate those needs into meaningful domain **schema** (e.g. using `protobuf`). Because user requirements can evolve, we **version** our schema (and thus our API) so we can support all users -- not just those who immediately adopt the latest version.

The specific things a user wants to do are referred to as **domain actions**, or simply **actions**.

When a customer requests new functionality, we either place it into an existing domain or create a new one. For example, if a user wants to execute a command on a machine in their network -- core functionality for this project -- we might model it as:

```protobuf
edition = "2023";
package external.core.run.v0; // 0 in this example as it is just an early draft

message RunRequest {
  string command = 1; // What to run
  string machine = 2; // Where to run it
}

message RunResponse {
  string result = 1; // Output from the terminal
}
```

In the `package`: `external` is the **root domain**, `core` is a **subdomain**, `run` is an **action**, and `v1` is the **schema version** (the *contract* with the customer). Together this may be referred to as the **domain path** or **package**. Everything above the action is the **software domain**.

## Internal Domain

The **internal domain** contains the system's own concerns: data storage, configuration and secrets, and developer-facing actions. It also contains **unversioned domain logic**, which can evolve over time and must be backwards-compatible so old API versions continue to function.

External domains often imply corresponding internal domains. For example: `example.internal.core.run` would contain the logic that implements the `external.core.run` action.

The connection between internal and external domains is made by a **service layer** or **API adapter** -- a versioned interface that translates between external request shapes (versioned, generated) and internal domain logic (unversioned, handwritten).

Typically, protobuf is used minimally in the internal domain; mostly for settings shape.

A nuance is that internal domain actions *may* be defined in protobuf, but they will generate CLIs instead of APIs.
