use axum_example::create_app;
use vespera::axum;

#[tokio::main]
async fn main() {
    let app = create_app();

    let addr = std::net::SocketAddr::from(([0, 0, 0, 0], 3000));
    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();

    println!("🚀 Server running on http://localhost:3000");

    axum::serve(listener, app).await.unwrap();
}
