# gRPC

**Category**: cncf
**Description**: High performance RPC framework
**Homepage**: https://grpc.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*gRPC Node.js packages*

- `@grpc/grpc-js` - Pure JS gRPC client
- `@grpc/proto-loader` - Protocol buffer loader
- `grpc` - Native gRPC (deprecated)

#### PYPI
*gRPC Python packages*

- `grpcio` - gRPC Python
- `grpcio-tools` - Protocol compiler
- `grpcio-reflection` - Reflection service
- `grpcio-health-checking` - Health checking

#### GO
*gRPC Go packages*

- `google.golang.org/grpc` - Go gRPC
- `google.golang.org/protobuf` - Protocol buffers
- `github.com/grpc-ecosystem/grpc-gateway` - REST gateway

#### MAVEN
*gRPC Java packages*

- `io.grpc:grpc-core` - Core library
- `io.grpc:grpc-netty` - Netty transport
- `io.grpc:grpc-stub` - Stub library
- `io.grpc:grpc-protobuf` - Protobuf integration

#### NUGET
*gRPC .NET packages*

- `Grpc.Net.Client` - .NET client
- `Grpc.AspNetCore` - ASP.NET Core
- `Google.Protobuf` - Protocol buffers

#### CARGO
*gRPC Rust packages*

- `tonic` - Rust gRPC
- `prost` - Protocol buffers

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate gRPC usage*

- `*.proto` - Protocol buffer files
- `buf.yaml` - Buf configuration
- `buf.gen.yaml` - Buf generation config

### Code Patterns

**Pattern**: `syntax\s*=\s*["']proto[23]["']`
- Protobuf syntax declaration
- Example: `syntax = "proto3";`

**Pattern**: `service\s+\w+\s*\{|rpc\s+\w+\s*\(`
- gRPC service definition
- Example: `service Greeter {\n  rpc SayHello`

**Pattern**: `message\s+\w+\s*\{`
- Protobuf message definition
- Example: `message HelloRequest {`

**Pattern**: `import\s+["']google/protobuf|google\.protobuf`
- Well-known types import
- Example: `import "google/protobuf/empty.proto";`

**Pattern**: `grpc\.(Dial|NewServer|Server)|grpc\.insecure`
- gRPC Go patterns
- Example: `conn, err := grpc.Dial(address)`

**Pattern**: `@GrpcService|@GrpcClient`
- gRPC annotations (Java/Micronaut)
- Example: `@GrpcService`

**Pattern**: `channel\.unary_unary|channel\.stream|stub\(`
- gRPC Python patterns
- Example: `stub = greeter_pb2_grpc.GreeterStub(channel)`

**Pattern**: `:50051|:9090`
- Common gRPC ports
- Example: `localhost:50051`

**Pattern**: `protoc|buf\s+generate|protoc-gen-`
- Protocol buffer compilation
- Example: `protoc --go_out=. *.proto`

---

## Environment Variables

- `GRPC_DEFAULT_SSL_ROOTS_FILE_PATH` - SSL roots file
- `GRPC_TRACE` - Trace logging
- `GRPC_VERBOSITY` - Verbosity level

## Detection Notes

- Uses HTTP/2 for transport
- Protocol Buffers for serialization
- Supports unary, streaming RPCs
- Health checking protocol
- Reflection for introspection

---

## Secrets Detection

### Credentials

#### gRPC TLS Certificate
**Pattern**: `pem_cert_chain|pem_root_certs`
**Severity**: high
**Description**: gRPC TLS certificate configuration

#### gRPC Channel Credentials
**Pattern**: `grpc\.ssl_channel_credentials\(.*private_key`
**Severity**: critical
**Description**: gRPC SSL channel credentials with private key

---

## TIER 3: Configuration Extraction

### Service Name Extraction

**Pattern**: `service\s+([A-Z][a-zA-Z0-9]+)\s*\{`
- gRPC service name
- Extracts: `service_name`
- Example: `service Greeter {`

### Package Name Extraction

**Pattern**: `package\s+([a-zA-Z0-9_.]+);`
- Protobuf package name
- Extracts: `package_name`
- Example: `package helloworld;`

### RPC Method Extraction

**Pattern**: `rpc\s+([A-Z][a-zA-Z0-9]+)\s*\(`
- RPC method name
- Extracts: `rpc_method`
- Example: `rpc SayHello (`
