# Tonic gRPC Service Patterns

## Proto Definition

```protobuf
// proto/user.proto
syntax = "proto3";
package user;

service UserService {
    rpc GetUser (GetUserRequest) returns (User);
    rpc ListUsers (ListUsersRequest) returns (stream User);
    rpc CreateUsers (stream CreateUserRequest) returns (CreateUsersResponse);
}

message User {
    int64 id = 1;
    string name = 2;
    string email = 3;
}

message GetUserRequest {
    int64 id = 1;
}

message ListUsersRequest {
    int32 page_size = 1;
}

message CreateUserRequest {
    string name = 1;
    string email = 2;
}

message CreateUsersResponse {
    int32 created_count = 1;
}
```

## Build Configuration

```rust
// build.rs
fn main() -> Result<(), Box<dyn std::error::Error>> {
    tonic_build::compile_protos("proto/user.proto")?;
    Ok(())
}
```

## Server Implementation

```rust
use tonic::{transport::Server, Request, Response, Status};
use user::user_service_server::{UserService, UserServiceServer};
use user::{User, GetUserRequest, ListUsersRequest, CreateUserRequest, CreateUsersResponse};
use tokio_stream::wrappers::ReceiverStream;

pub mod user {
    tonic::include_proto!("user");
}

#[derive(Default)]
pub struct MyUserService {}

#[tonic::async_trait]
impl UserService for MyUserService {
    // Unary RPC
    async fn get_user(
        &self,
        request: Request<GetUserRequest>,
    ) -> Result<Response<User>, Status> {
        let req = request.into_inner();
        
        // Simulated lookup
        let user = User {
            id: req.id,
            name: "John".into(),
            email: "john@example.com".into(),
        };
        
        Ok(Response::new(user))
    }

    // Server streaming
    type ListUsersStream = ReceiverStream<Result<User, Status>>;

    async fn list_users(
        &self,
        request: Request<ListUsersRequest>,
    ) -> Result<Response<Self::ListUsersStream>, Status> {
        let (tx, rx) = tokio::sync::mpsc::channel(4);
        
        tokio::spawn(async move {
            for i in 0..10 {
                let user = User {
                    id: i,
                    name: format!("User {}", i),
                    email: format!("user{}@example.com", i),
                };
                tx.send(Ok(user)).await.unwrap();
            }
        });

        Ok(Response::new(ReceiverStream::new(rx)))
    }

    // Client streaming
    async fn create_users(
        &self,
        request: Request<tonic::Streaming<CreateUserRequest>>,
    ) -> Result<Response<CreateUsersResponse>, Status> {
        let mut stream = request.into_inner();
        let mut count = 0;

        while let Some(req) = stream.message().await? {
            println!("Creating user: {}", req.name);
            count += 1;
        }

        Ok(Response::new(CreateUsersResponse { created_count: count }))
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let addr = "[::1]:50051".parse()?;
    let service = MyUserService::default();

    Server::builder()
        .add_service(UserServiceServer::new(service))
        .serve(addr)
        .await?;

    Ok(())
}
```

## Client Implementation

```rust
use user::user_service_client::UserServiceClient;
use user::GetUserRequest;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut client = UserServiceClient::connect("http://[::1]:50051").await?;

    // Unary call
    let request = tonic::Request::new(GetUserRequest { id: 1 });
    let response = client.get_user(request).await?;
    println!("User: {:?}", response.into_inner());

    // Server streaming
    let request = tonic::Request::new(ListUsersRequest { page_size: 10 });
    let mut stream = client.list_users(request).await?.into_inner();
    
    while let Some(user) = stream.message().await? {
        println!("Received: {:?}", user);
    }

    Ok(())
}
```

## Interceptors

```rust
use tonic::{Request, Status};

fn auth_interceptor(mut req: Request<()>) -> Result<Request<()>, Status> {
    let token = req.metadata()
        .get("authorization")
        .and_then(|t| t.to_str().ok());

    match token {
        Some(t) if validate_token(t) => Ok(req),
        _ => Err(Status::unauthenticated("Invalid token")),
    }
}

// Apply to server
Server::builder()
    .add_service(UserServiceServer::with_interceptor(service, auth_interceptor))
    .serve(addr)
    .await?;

// Apply to client
let channel = Channel::from_static("http://[::1]:50051").connect().await?;
let client = UserServiceClient::with_interceptor(channel, |mut req: Request<()>| {
    req.metadata_mut().insert("authorization", "Bearer token".parse().unwrap());
    Ok(req)
});
```

## Error Handling

```rust
use tonic::Status;

async fn get_user(&self, request: Request<GetUserRequest>) -> Result<Response<User>, Status> {
    let id = request.into_inner().id;
    
    if id <= 0 {
        return Err(Status::invalid_argument("ID must be positive"));
    }
    
    match self.db.find_user(id).await {
        Ok(Some(user)) => Ok(Response::new(user)),
        Ok(None) => Err(Status::not_found(format!("User {} not found", id))),
        Err(e) => Err(Status::internal(format!("Database error: {}", e))),
    }
}
```
