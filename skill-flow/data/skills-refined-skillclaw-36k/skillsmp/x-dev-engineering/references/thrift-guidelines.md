# Reference: Communication & Thrift Guidelines

X uses **Apache Thrift** as its Interface Definition Language (IDL) to maintain a strict contract between Scala orchestration and Rust execution.

### Best Practices
1.  **Strict ID Management:** Never change an existing field ID. New engagement signals for the Phoenix model must be added as new optional IDs to maintain backward compatibility.
2.  **Thin Objects:** Sourcing and retrieval layers should pass only IDs and minimal features through Thrift. Full hydration (text/media) should happen as late as possible in the pipeline.
3.  **Schema Definitions:**
    * `request.thrift`: Defines the `MixerRequest` including user context.
    * `ranking.thrift`: Contains the multi-action engagement labels (Like, Repost, etc.) predicted by the transformer.
