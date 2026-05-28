# Temporal-Cloud - Certificates

**Pages:** 8

---

## Alternatively, run npm ci, which installs only dependencies specified in the lock file and is generally faster.

**URL:** llms-txt#alternatively,-run-npm-ci,-which-installs-only-dependencies-specified-in-the-lock-file-and-is-generally-faster.

**Contents:**
  - Using `node:slim` images

RUN npm install --only=production \
    && npm run build

CMD ["npm", "start"]
dockerfile
FROM node:20-bullseye-slim

RUN apt-get update \
    && apt-get install -y ca-certificates \
    && rm -rf /var/lib/apt/lists/*

**Examples:**

Example 1 (unknown):
```unknown
For smaller images and/or more secure deployments, it is also possible to use `-slim` Docker image variants (like `node:20-bullseye-slim`) or `distroless/nodejs` Docker images (like `gcr.io/distroless/nodejs20-debian11`) with the following caveats.

### Using `node:slim` images

`node:slim` images do not contain some of the common packages found in regular images. This results in significantly smaller images.

However, TypeScript SDK requires the presence of root TLS certificates (the `ca-certificates` package), which are not included in `slim` images.
The `ca-certificates` package is required even when connecting to a local Temporal Server or when using a server connection config that doesn't explicitly use TLS.

For this reason, the `ca-certificates` package must be installed during the construction of the Docker image.
For example:
```

---

## Use certificate files for mTLS

**URL:** llms-txt#use-certificate-files-for-mtls

client_cert_path = "/etc/temporal/certs/client.pem"
client_key_path = "/etc/temporal/certs/client.key"

---

## TLS is auto-enabled when this TLS config or API key is present, but you can configure it explicitly

**URL:** llms-txt#tls-is-auto-enabled-when-this-tls-config-or-api-key-is-present,-but-you-can-configure-it-explicitly

---

## Optional TLS overrides (only needed when you must pin certs or tweak SNI)

**URL:** llms-txt#optional-tls-overrides-(only-needed-when-you-must-pin-certs-or-tweak-sni)

temporal --profile prod config set --prop tls.server_name --value "<namespace_id>.<account_id>"
temporal --profile prod config set --prop tls.ca_cert_path --value "/path/to/ca.pem"

---

## TLS configuration for production

**URL:** llms-txt#tls-configuration-for-production

---

## Example of providing certificate data directly (base64 or PEM format)

**URL:** llms-txt#example-of-providing-certificate-data-directly-(base64-or-pem-format)

**Contents:**
- CLI integration

client_cert_data = """-----BEGIN CERTIFICATE-----
MIICertificateDataHere...
-----END CERTIFICATE-----"""
client_key_data = """-----BEGIN PRIVATE KEY-----
MIIPrivateKeyDataHere...
-----END PRIVATE KEY-----"""
bash

**Examples:**

Example 1 (unknown):
```unknown
## CLI integration

The Temporal CLI tool includes `temporal config` commands that allow you to read and write to the TOML configuration
file. This provides a convenient way to manage your connection profiles without manually editing the file. Refer to
[Temporal CLI Reference - `temporal config`](../cli/config.mdx) for more details.

- `temporal config get <property>`: Reads a specific value from the current profile.
- `temporal config set <property> <value>`: Sets a property in the current profile.
- `temporal config delete <property>`: Deletes a property from the current profile.
- `temporal config list`: Lists all available profiles in the config file.

These CLI commands directly manipulate the `temporal.toml` file. This differs from the SDKs, which only _read_ from the
file and environment at runtime to establish a client connection. You can select a profile for the CLI to use with the
`--profile` flag. For example, `temporal --profile prod ...`.

The following code blocks provide copy-paste-friendly examples for setting up CLI profiles for both local development
and Temporal Cloud.

<Tabs groupId="cli-profile-setup" defaultValue="api-key-basic">
  <TabItem value="api-key-basic" label="Local + Prod with Cloud API key">

This example shows how to set up a default profile for local development and a `prod` profile for Temporal Cloud using
an API key.
```

---

## TLS auto-enables when TLS config or an API key is present

**URL:** llms-txt#tls-auto-enables-when-tls-config-or-an-api-key-is-present

---

## Staging profile with inline certificate data

**URL:** llms-txt#staging-profile-with-inline-certificate-data

[profile.staging]
address = "staging.temporal.example.com:7233"
namespace = "staging"

[profile.staging.tls]

---
