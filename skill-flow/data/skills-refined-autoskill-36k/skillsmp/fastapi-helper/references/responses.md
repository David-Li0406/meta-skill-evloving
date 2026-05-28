# FastAPI Responses Reference

## Response Classes

```python
from fastapi import Response
from fastapi.responses import (
    JSONResponse,
    HTMLResponse,
    PlainTextResponse,
    RedirectResponse,
    StreamingResponse,
    FileResponse
)

# Default JSON response
@app.get("/items/")
async def read_items():
    return {"items": []}  # Automatically JSONResponse

# Explicit JSONResponse
@app.get("/items/")
async def read_items():
    return JSONResponse(
        content={"items": []},
        status_code=200,
        headers={"X-Custom": "value"},
        media_type="application/json"
    )

# HTML Response
@app.get("/html/", response_class=HTMLResponse)
async def get_html():
    return "<html><body><h1>Hello</h1></body></html>"

# Plain Text
@app.get("/text/", response_class=PlainTextResponse)
async def get_text():
    return "Hello, World!"

# Redirect
@app.get("/redirect/")
async def redirect():
    return RedirectResponse(url="/items/", status_code=307)

# File Response
@app.get("/file/")
async def get_file():
    return FileResponse(
        path="file.pdf",
        filename="download.pdf",
        media_type="application/pdf"
    )

# Streaming Response
@app.get("/stream/")
async def stream():
    async def generate():
        for i in range(10):
            yield f"data: {i}\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream")
```

## Response Model

```python
from pydantic import BaseModel

class ItemOut(BaseModel):
    name: str
    price: float
    # password field excluded from response

@app.post("/items/", response_model=ItemOut)
async def create_item(item: ItemIn):
    return item  # Filters to only ItemOut fields

# Exclude unset values
@app.get("/items/", response_model=Item, response_model_exclude_unset=True)
async def read_item():
    return item

# Include/exclude specific fields
@app.get("/items/", response_model=Item, response_model_include={"name", "price"})
@app.get("/items/", response_model=Item, response_model_exclude={"password"})
```

## Custom Response Headers & Cookies

```python
from fastapi import Response

@app.get("/items/")
async def read_items(response: Response):
    response.headers["X-Custom-Header"] = "custom-value"
    response.set_cookie(key="session", value="abc123", httponly=True)
    return {"items": []}

# Delete cookie
@app.get("/logout/")
async def logout(response: Response):
    response.delete_cookie(key="session")
    return {"message": "logged out"}
```

## Status Codes

```python
from fastapi import status

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    return None

# Common status codes
status.HTTP_200_OK
status.HTTP_201_CREATED
status.HTTP_204_NO_CONTENT
status.HTTP_400_BAD_REQUEST
status.HTTP_401_UNAUTHORIZED
status.HTTP_403_FORBIDDEN
status.HTTP_404_NOT_FOUND
status.HTTP_422_UNPROCESSABLE_ENTITY
status.HTTP_500_INTERNAL_SERVER_ERROR
```
