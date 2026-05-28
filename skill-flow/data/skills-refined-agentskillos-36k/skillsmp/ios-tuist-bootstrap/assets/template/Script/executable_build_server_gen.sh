#!/bin/bash

# This script will install dependencies & generate the workspace. It then creates a
# build server configuration for the workspace, which enables editors other than
# Xcode to provide code completion etc via the swift language server.
tuist install --force-resolved-versions && \
    tuist generate --no-open && \
    tuist test --build-only && \
    xcode-build-server config -scheme {{SCHEME_NAME}} -workspace {{WORKSPACE_NAME}}
