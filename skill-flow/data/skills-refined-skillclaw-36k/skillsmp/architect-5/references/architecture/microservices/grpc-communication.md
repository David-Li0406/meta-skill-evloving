# gRPC Communication Patterns

**Category**: architecture/microservices
**Description**: Detect gRPC client/server definitions for service mapping
**Purpose**: Map gRPC-based microservice dependencies

---

## Proto File Detection

### Service Definition
**Type**: regex
**Severity**: info
**Pattern**: `service\s+(\w+)\s*\{`
- gRPC service definition in .proto files
- Example: `service UserService {`
- Captures: Service name

### RPC Method Definition
**Type**: regex
**Severity**: info
**Pattern**: `rpc\s+(\w+)\s*\(\s*(\w+)\s*\)\s*returns\s*\(\s*(\w+)\s*\)`
- RPC method signature
- Example: `rpc GetUser (GetUserRequest) returns (User)`
- Captures: Method, request type, response type

### Package Declaration
**Type**: regex
**Severity**: info
**Pattern**: `package\s+([\w.]+)\s*;`
- Proto package name
- Example: `package com.example.user.v1;`
- Captures: Package namespace

### Import Statement
**Type**: regex
**Severity**: info
**Pattern**: `import\s+["']([^"']+\.proto)["']\s*;`
- Proto imports (cross-service dependencies)
- Example: `import "common/types.proto";`
- Captures: Imported file path

---

## Python gRPC

### gRPC Channel Creation
**Type**: semgrep
**Severity**: info
**Languages**: [python]
**Pattern**: `grpc.insecure_channel($TARGET)`
- Creates insecure gRPC channel
- Example: `grpc.insecure_channel('user-service:50051')`
- Captures: Target service address

### Secure Channel Creation
**Type**: semgrep
**Severity**: info
**Languages**: [python]
**Pattern**: `grpc.secure_channel($TARGET, ...)`
- Creates secure gRPC channel with credentials
- Example: `grpc.secure_channel('user-service:443', credentials)`

### Stub Creation
**Type**: semgrep
**Severity**: info
**Languages**: [python]
**Pattern**: `$SERVICE_pb2_grpc.$STUBStub($CHANNEL)`
- Creates gRPC client stub
- Example: `user_pb2_grpc.UserServiceStub(channel)`
- Captures: Service stub name

### Async Stub Creation
**Type**: semgrep
**Severity**: info
**Languages**: [python]
**Pattern**: `$SERVICE_pb2_grpc.$STUBAsyncStub($CHANNEL)`
- Creates async gRPC client stub
- Example: `user_pb2_grpc.UserServiceAsyncStub(channel)`

### Server Add Service
**Type**: semgrep
**Severity**: info
**Languages**: [python]
**Pattern**: `$SERVICE_pb2_grpc.add_$SERVICEServicer_to_server(...)`
- Registers gRPC service implementation
- Example: `user_pb2_grpc.add_UserServiceServicer_to_server(UserServicer(), server)`

---

## Go gRPC

### Dial Connection
**Type**: semgrep
**Severity**: info
**Languages**: [go]
**Pattern**: `grpc.Dial($TARGET, ...)`
- Creates gRPC client connection
- Example: `grpc.Dial("user-service:50051", grpc.WithInsecure())`

### NewClient Connection
**Type**: semgrep
**Severity**: info
**Languages**: [go]
**Pattern**: `grpc.NewClient($TARGET, ...)`
- New style gRPC client (Go 1.21+)
- Example: `grpc.NewClient("dns:///user-service:50051")`

### Client Creation
**Type**: semgrep
**Severity**: info
**Languages**: [go]
**Pattern**: `$PKG.New$SERVICEClient($CONN)`
- Creates typed gRPC client
- Example: `userpb.NewUserServiceClient(conn)`
- Captures: Service client type

### Register Server
**Type**: semgrep
**Severity**: info
**Languages**: [go]
**Pattern**: `$PKG.Register$SERVICEServer($SERVER, ...)`
- Registers gRPC service
- Example: `userpb.RegisterUserServiceServer(grpcServer, &userServer{})`

---

## JavaScript/TypeScript gRPC

### gRPC-js Client
**Type**: semgrep
**Severity**: info
**Languages**: [javascript, typescript]
**Pattern**: `new $PKG.$SERVICE($TARGET, ...)`
- Creates gRPC-js client
- Example: `new userProto.UserService('localhost:50051', grpc.credentials.createInsecure())`

### gRPC-web Client
**Type**: semgrep
**Severity**: info
**Languages**: [javascript, typescript]
**Pattern**: `new $SERVICEClient($TARGET, ...)`
- Creates gRPC-web client
- Example: `new UserServiceClient('http://envoy-proxy:8080')`

### Connect-es Client
**Type**: semgrep
**Severity**: info
**Languages**: [javascript, typescript]
**Pattern**: `createPromiseClient($SERVICE, $TRANSPORT)`
- Connect protocol client
- Example: `createPromiseClient(UserService, transport)`

---

## Java gRPC

### Channel Builder
**Type**: semgrep
**Severity**: info
**Languages**: [java]
**Pattern**: `ManagedChannelBuilder.forAddress($HOST, $PORT)...`
- Creates gRPC managed channel
- Example: `ManagedChannelBuilder.forAddress("user-service", 50051).usePlaintext().build()`

### Channel For Target
**Type**: semgrep
**Severity**: info
**Languages**: [java]
**Pattern**: `ManagedChannelBuilder.forTarget($TARGET)...`
- Creates gRPC channel with target string
- Example: `ManagedChannelBuilder.forTarget("dns:///user-service:50051")`

### Stub Creation
**Type**: semgrep
**Severity**: info
**Languages**: [java]
**Pattern**: `$SERVICEGrpc.newBlockingStub($CHANNEL)`
- Creates blocking gRPC stub
- Example: `UserServiceGrpc.newBlockingStub(channel)`

### Async Stub
**Type**: semgrep
**Severity**: info
**Languages**: [java]
**Pattern**: `$SERVICEGrpc.newStub($CHANNEL)`
- Creates async gRPC stub
- Example: `UserServiceGrpc.newStub(channel)`

### Bind Service
**Type**: semgrep
**Severity**: info
**Languages**: [java]
**Pattern**: `$SERVER.addService($SERVICE.bindService(...))`
- Binds gRPC service to server
- Example: `serverBuilder.addService(userService.bindService())`

---

## gRPC Target Patterns

### Direct Target
**Type**: regex
**Severity**: info
**Pattern**: `(?:dns:///)?([a-z0-9-]+(?:\.[a-z0-9-]+)*)(?::(\d+))?`
- Direct gRPC target address
- Example: `user-service:50051` or `dns:///user-service:50051`
- Captures: Host, port

### Kubernetes DNS Target
**Type**: regex
**Severity**: info
**Pattern**: `(?:dns:///)?([a-z0-9-]+)\.([a-z0-9-]+)(?:\.svc(?:\.cluster\.local)?)?:(\d+)`
- Kubernetes service DNS
- Example: `user-service.production.svc.cluster.local:50051`
- Captures: Service, namespace, port

---

## Detection Confidence

**Proto Analysis**: 95%
**Code Pattern Detection**: 90%

---

## References

- gRPC Documentation
- Protocol Buffers Language Guide
- gRPC Best Practices
