# Fastapi - Api

**Pages:** 2

---

## FastAPI¶

**URL:** https://fastapi.tiangolo.com/

**Contents:**
- FastAPI¶
- Sponsors¶
  - Keystone Sponsor¶
  - Gold and Silver Sponsors¶
- Opinions¶
- FastAPI mini documentary¶
- Typer, the FastAPI of CLIs¶
- Requirements¶
- Installation¶
- Example¶

FastAPI framework, high performance, easy to learn, fast to code, ready for production

Documentation: https://fastapi.tiangolo.com

Source Code: https://github.com/fastapi/fastapi

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python based on standard Python type hints.

The key features are:

* estimation based on tests conducted by an internal development team, building production applications.

"[...] I'm using FastAPI a ton these days. [...] I'm actually planning to use it for all of my team's ML services at Microsoft. Some of them are getting integrated into the core Windows product and some Office products."

"We adopted the FastAPI library to spawn a REST server that can be queried to obtain predictions. [for Ludwig]"

"Netflix is pleased to announce the open-source release of our crisis management orchestration framework: Dispatch! [built with FastAPI]"

"I’m over the moon excited about FastAPI. It’s so fun!"

"Honestly, what you've built looks super solid and polished. In many ways, it's what I wanted Hug to be - it's really inspiring to see someone build that."

"If you're looking to learn one modern framework for building REST APIs, check out FastAPI [...] It's fast, easy to use and easy to learn [...]"

"We've switched over to FastAPI for our APIs [...] I think you'll like it [...]"

"If anyone is looking to build a production Python API, I would highly recommend FastAPI. It is beautifully designed, simple to use and highly scalable, it has become a key component in our API first development strategy and is driving many automations and services such as our Virtual TAC Engineer."

There's a FastAPI mini documentary released at the end of 2025, you can watch it online:

If you are building a CLI app to be used in the terminal instead of a web API, check out Typer.

Typer is FastAPI's little sibling. And it's intended to be the FastAPI of CLIs. ⌨️ 🚀

FastAPI stands on the shoulders of giants:

Create and activate a virtual environment and then install FastAPI:

Note: Make sure you put "fastapi[standard]" in quotes to ensure it works in all terminals.

Create a file main.py with:

If your code uses async / await, use async def:

If you don't know, check the "In a hurry?" section about async and await in the docs.

The command fastapi dev reads your main.py file, detects the FastAPI app in it, and starts a server using Uvicorn.

By default, fastapi dev will start with auto-reload enabled for local development.

You can read more about it in the FastAPI CLI docs.

Open your browser at http://127.0.0.1:8000/items/5?q=somequery.

You will see the JSON response as:

You already created an API that:

Now go to http://127.0.0.1:8000/docs.

You will see the automatic interactive API documentation (provided by Swagger UI):

And now, go to http://127.0.0.1:8000/redoc.

You will see the alternative automatic documentation (provided by ReDoc):

Now modify the file main.py to receive a body from a PUT request.

Declare the body using standard Python types, thanks to Pydantic.

The fastapi dev server should reload automatically.

Now go to http://127.0.0.1:8000/docs.

And now, go to http://127.0.0.1:8000/redoc.

In summary, you declare once the types of parameters, body, etc. as function parameters.

You do that with standard modern Python types.

You don't have to learn a new syntax, the methods or classes of a specific library, etc.

Just standard Python.

For example, for an int:

or for a more complex Item model:

...and with that single declaration you get:

Coming back to the previous code example, FastAPI will:

We just scratched the surface, but you already get the idea of how it all works.

Try changing the line with:

...and see how your editor will auto-complete the attributes and know their types:

For a more complete example including more features, see the Tutorial - User Guide.

Spoiler alert: the tutorial - user guide includes:

You can optionally deploy your FastAPI app to FastAPI Cloud, go and join the waiting list if you haven't. 🚀

If you already have a FastAPI Cloud account (we invited you from the waiting list 😉), you can deploy your application with one command.

Before deploying, make sure you are logged in:

Then deploy your app:

That's it! Now you can access your app at that URL. ✨

FastAPI Cloud is built by the same author and team behind FastAPI.

It streamlines the process of building, deploying, and accessing an API with minimal effort.

It brings the same developer experience of building apps with FastAPI to deploying them to the cloud. 🎉

FastAPI Cloud is the primary sponsor and funding provider for the FastAPI and friends open source projects. ✨

FastAPI is open source and based on standards. You can deploy FastAPI apps to any cloud provider you choose.

Follow your cloud provider's guides to deploy FastAPI apps with them. 🤓

Independent TechEmpower benchmarks show FastAPI applications running under Uvicorn as one of the fastest Python frameworks available, only below Starlette and Uvicorn themselves (used internally by FastAPI). (*)

To understand more about it, see the section Benchmarks.

FastAPI depends on Pydantic and Starlette.

When you install FastAPI with pip install "fastapi[standard]" it comes with the standard group of optional dependencies:

If you don't want to include the standard optional dependencies, you can install with pip install fastapi instead of pip install "fastapi[standard]".

If you want to install FastAPI with the standard dependencies but without the fastapi-cloud-cli, you can install with pip install "fastapi[standard-no-fastapi-cloud-cli]".

There are some additional dependencies you might want to install.

Additional optional Pydantic dependencies:

Additional optional FastAPI dependencies:

This project is licensed under the terms of the MIT license.

**Examples:**

Example 1 (php):
```php
$ pip install "fastapi[standard]"

---> 100%
```

Example 2 (python):
```python
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

Example 3 (python):
```python
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

Example 4 (yaml):
```yaml
$ fastapi dev main.py

 ╭────────── FastAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8000                  │
 │                                                     │
 │  API docs: http://127.0.0.1:8000/docs               │
 │                                                     │
 │  Running in development mode, for production use:   │
 │                                                     │
 │  fastapi run                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

INFO:     Will watch for changes in these directories: ['/home/user/code/awesomeapp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [2248755] using WatchFiles
INFO:     Started server process [2248757]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## Reference¶

**URL:** https://fastapi.tiangolo.com/reference/

**Contents:**
- Reference¶

Here's the reference or code API, the classes, functions, parameters, attributes, and all the FastAPI parts you can use in your applications.

If you want to learn FastAPI you are much better off reading the FastAPI Tutorial.

---
