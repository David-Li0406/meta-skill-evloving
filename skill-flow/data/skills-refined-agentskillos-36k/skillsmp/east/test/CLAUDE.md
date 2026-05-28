# East compliance tests

This test suite is self-hosted and runs on an East platform providing basic test functionality.
It exists separately to the unit tests in ../src for the purpose of testing both this and other East runtimes.

Each test can be serialized to IR and executed on any runtime providing the minimal test platform.
This acts as a compliance suite we can use to help implement East runtimes in other languages - for example those targetting fast, static compilation.
