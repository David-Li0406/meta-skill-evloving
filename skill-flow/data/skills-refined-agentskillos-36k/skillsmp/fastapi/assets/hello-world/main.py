"""
Minimal FastAPI Hello World Application

This is the simplest possible FastAPI application.
Perfect for getting started and understanding the basics.
"""

from fastapi import FastAPI

app = FastAPI(title="Hello World API", version="1.0.0")


@app.get("/")
async def root():
    """Root endpoint - returns a welcome message."""
    return {"message": "Hello World"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    """Example endpoint with path and query parameters."""
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
