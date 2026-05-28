use axum::{
    http::{header, HeaderValue, Request, StatusCode},
    middleware::Next,
    response::Response,
};
use tower_http::cors::{Any, CorsLayer};

pub fn cors_layer() -> CorsLayer {
    CorsLayer::new()
        .allow_origin("http://localhost:3000".parse::<HeaderValue>().unwrap())
        .allow_methods([
            http::Method::GET,
            http::Method::POST,
            http::Method::PUT,
            http::Method::DELETE,
        ])
        .allow_headers([header::CONTENT_TYPE, header::AUTHORIZATION])
        .allow_credentials(true)
}

pub async fn security_headers<B>(
    req: Request<B>,
    next: Next<B>,
) -> Result<Response, StatusCode> {
    let mut response = next.run(req).await;
    let headers = response.headers_mut();

    // CSP
    headers.insert(
        header::CONTENT_SECURITY_POLICY,
        HeaderValue::from_static(
            "default-src 'self'; \
             script-src 'self'; \
             style-src 'self' 'unsafe-inline'; \
             img-src 'self' data: https:; \
             font-src 'self'; \
             connect-src 'self'; \
             frame-ancestors 'none';"
        ),
    );

    // HSTS
    headers.insert(
        header::STRICT_TRANSPORT_SECURITY,
        HeaderValue::from_static("max-age=31536000; includeSubDomains; preload"),
    );

    // Other headers
    headers.insert(
        header::X_CONTENT_TYPE_OPTIONS,
        HeaderValue::from_static("nosniff"),
    );

    headers.insert(
        header::X_FRAME_OPTIONS,
        HeaderValue::from_static("DENY"),
    );

    headers.insert(
        "Referrer-Policy",
        HeaderValue::from_static("strict-origin-when-cross-origin"),
    );

    Ok(response)
}
