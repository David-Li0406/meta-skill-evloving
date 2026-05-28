# Build and Java 17 Compatibility

This note documents the current build.gradle change for JDK 17 compatibility and the rationale for using Atomikos.

## build.gradle Change (Spark on Newer JDKs)

File: `build.gradle`

Change summary:
- Adds `--add-exports=java.base/sun.nio.ch=ALL-UNNAMED` to all `JavaForkOptions` tasks.
- Keeps Spark jobs working on JDK 17 where access to `sun.nio.ch` is otherwise blocked by the module system.

Why this is needed:
- Spark relies on internal JDK classes in `sun.nio.ch` for certain I/O paths.
- JDK 17 enforces module boundaries, so the export is required to avoid illegal access errors.

## Why Atomikos for Java 17

Moqui defaults to Bitronix for the internal transaction manager:
- Config: `framework/src/main/resources/MoquiDefaultConf.xml` (`TransactionInternalBitronix`)
- Dependency: `framework/build.gradle` (`org.codehaus.btm:btm`)

For Java 17 compatibility we standardize on Atomikos because:
- Bitronix is old and not maintained for newer JDKs and module restrictions.
- Atomikos provides a maintained JTA implementation that is known to work on modern JDKs.

Current repo signals:
- Atomikos loggers are already defined in `framework/src/main/resources/log4j2.xml`.
- Test references exist in `framework/src/test/groovy/TransactionFacadeTests.groovy`.

If/when we switch:
- Add Atomikos dependencies in `framework/build.gradle`.
- Wire an Atomikos transaction manager implementation.
- Update `framework/src/main/resources/MoquiDefaultConf.xml` to use the Atomikos internal transaction class.
