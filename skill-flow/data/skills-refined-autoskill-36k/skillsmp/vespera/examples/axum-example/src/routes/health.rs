#[vespera::route(get)]
pub async fn health() -> &'static str {
    "ok"
}
