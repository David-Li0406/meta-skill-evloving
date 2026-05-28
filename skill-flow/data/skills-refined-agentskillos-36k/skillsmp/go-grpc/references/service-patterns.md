# gRPC Service Patterns

## Proto Definition

```protobuf
// user.proto
syntax = "proto3";

package user;

option go_package = "github.com/example/myapp/proto/user";

service UserService {
    // Unary RPC
    rpc GetUser(GetUserRequest) returns (User);
    rpc CreateUser(CreateUserRequest) returns (User);
    
    // Server streaming
    rpc ListUsers(ListUsersRequest) returns (stream User);
    
    // Client streaming
    rpc UploadUsers(stream User) returns (UploadResponse);
    
    // Bidirectional streaming
    rpc Chat(stream ChatMessage) returns (stream ChatMessage);
}

message User {
    string id = 1;
    string name = 2;
    string email = 3;
    int32 age = 4;
}

message GetUserRequest {
    string id = 1;
}

message CreateUserRequest {
    string name = 1;
    string email = 2;
    int32 age = 3;
}

message ListUsersRequest {
    int32 page_size = 1;
    string page_token = 2;
}

message UploadResponse {
    int32 count = 1;
}

message ChatMessage {
    string user_id = 1;
    string content = 2;
}
```

## Server Implementation

```go
import (
    "context"
    "net"
    "google.golang.org/grpc"
    "google.golang.org/grpc/codes"
    "google.golang.org/grpc/status"
    pb "github.com/example/myapp/proto/user"
)

type userServer struct {
    pb.UnimplementedUserServiceServer
    db *Database
}

// Unary RPC
func (s *userServer) GetUser(ctx context.Context, req *pb.GetUserRequest) (*pb.User, error) {
    user, err := s.db.FindUser(req.Id)
    if err != nil {
        return nil, status.Errorf(codes.NotFound, "user not found: %v", err)
    }
    
    return &pb.User{
        Id:    user.ID,
        Name:  user.Name,
        Email: user.Email,
        Age:   int32(user.Age),
    }, nil
}

func (s *userServer) CreateUser(ctx context.Context, req *pb.CreateUserRequest) (*pb.User, error) {
    if req.Name == "" {
        return nil, status.Error(codes.InvalidArgument, "name is required")
    }
    
    user, err := s.db.CreateUser(req.Name, req.Email, int(req.Age))
    if err != nil {
        return nil, status.Errorf(codes.Internal, "failed to create user: %v", err)
    }
    
    return &pb.User{
        Id:    user.ID,
        Name:  user.Name,
        Email: user.Email,
        Age:   int32(user.Age),
    }, nil
}

// Server streaming
func (s *userServer) ListUsers(req *pb.ListUsersRequest, stream pb.UserService_ListUsersServer) error {
    users, err := s.db.ListUsers(int(req.PageSize))
    if err != nil {
        return status.Errorf(codes.Internal, "failed to list users: %v", err)
    }
    
    for _, user := range users {
        if err := stream.Send(&pb.User{
            Id:    user.ID,
            Name:  user.Name,
            Email: user.Email,
        }); err != nil {
            return err
        }
    }
    
    return nil
}

// Start server
func main() {
    lis, err := net.Listen("tcp", ":50051")
    if err != nil {
        log.Fatalf("failed to listen: %v", err)
    }
    
    grpcServer := grpc.NewServer()
    pb.RegisterUserServiceServer(grpcServer, &userServer{db: db})
    
    log.Println("gRPC server listening on :50051")
    if err := grpcServer.Serve(lis); err != nil {
        log.Fatalf("failed to serve: %v", err)
    }
}
```

## Client Implementation

```go
import (
    "context"
    "io"
    "google.golang.org/grpc"
    "google.golang.org/grpc/credentials/insecure"
    pb "github.com/example/myapp/proto/user"
)

func main() {
    conn, err := grpc.Dial("localhost:50051",
        grpc.WithTransportCredentials(insecure.NewCredentials()),
    )
    if err != nil {
        log.Fatalf("failed to connect: %v", err)
    }
    defer conn.Close()
    
    client := pb.NewUserServiceClient(conn)
    
    // Unary call
    ctx := context.Background()
    user, err := client.GetUser(ctx, &pb.GetUserRequest{Id: "123"})
    if err != nil {
        log.Fatalf("GetUser failed: %v", err)
    }
    log.Printf("User: %v", user)
    
    // Server streaming
    stream, err := client.ListUsers(ctx, &pb.ListUsersRequest{PageSize: 10})
    if err != nil {
        log.Fatalf("ListUsers failed: %v", err)
    }
    
    for {
        user, err := stream.Recv()
        if err == io.EOF {
            break
        }
        if err != nil {
            log.Fatalf("stream error: %v", err)
        }
        log.Printf("User: %v", user)
    }
}
```

## Interceptors (Middleware)

```go
// Unary interceptor
func loggingInterceptor(
    ctx context.Context,
    req interface{},
    info *grpc.UnaryServerInfo,
    handler grpc.UnaryHandler,
) (interface{}, error) {
    start := time.Now()
    
    resp, err := handler(ctx, req)
    
    log.Printf("Method: %s, Duration: %v, Error: %v",
        info.FullMethod, time.Since(start), err)
    
    return resp, err
}

// Stream interceptor
func streamLoggingInterceptor(
    srv interface{},
    ss grpc.ServerStream,
    info *grpc.StreamServerInfo,
    handler grpc.StreamHandler,
) error {
    log.Printf("Stream started: %s", info.FullMethod)
    err := handler(srv, ss)
    log.Printf("Stream ended: %s, Error: %v", info.FullMethod, err)
    return err
}

// Apply interceptors
grpcServer := grpc.NewServer(
    grpc.UnaryInterceptor(loggingInterceptor),
    grpc.StreamInterceptor(streamLoggingInterceptor),
)
```

## Error Handling

```go
import (
    "google.golang.org/grpc/codes"
    "google.golang.org/grpc/status"
)

// Server-side
func (s *server) GetUser(ctx context.Context, req *pb.GetUserRequest) (*pb.User, error) {
    if req.Id == "" {
        return nil, status.Error(codes.InvalidArgument, "id is required")
    }
    
    user, err := s.db.FindUser(req.Id)
    if err == ErrNotFound {
        return nil, status.Errorf(codes.NotFound, "user %s not found", req.Id)
    }
    if err != nil {
        return nil, status.Errorf(codes.Internal, "database error: %v", err)
    }
    
    return user, nil
}

// Client-side
user, err := client.GetUser(ctx, req)
if err != nil {
    st, ok := status.FromError(err)
    if ok {
        switch st.Code() {
        case codes.NotFound:
            log.Printf("User not found")
        case codes.InvalidArgument:
            log.Printf("Invalid request: %s", st.Message())
        default:
            log.Printf("Error: %v", st.Message())
        }
    }
}
```
