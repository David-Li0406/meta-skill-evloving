# Python Dependency Categories

Reference for categorizing Python imports during skill migration analysis.

## Standard Library (no install needed)

```
abc, argparse, ast, asyncio, base64, bisect, calendar,
collections, concurrent, configparser, contextlib, copy,
csv, dataclasses, datetime, decimal, difflib, email,
enum, errno, fnmatch, fractions, functools, gc, getpass,
glob, gzip, hashlib, heapq, html, http, importlib, inspect,
io, itertools, json, locale, logging, math, mimetypes,
multiprocessing, numbers, operator, os, pathlib, pickle,
platform, pprint, queue, random, re, secrets, select, shlex,
shutil, signal, socket, sqlite3, ssl, stat, statistics,
string, struct, subprocess, sys, tempfile, textwrap,
threading, time, timeit, traceback, types, typing,
unicodedata, unittest, urllib, uuid, warnings, weakref,
xml, zipfile, zlib
```

## Common Third-Party (pip install required)

| Package | Description | Install |
|---------|-------------|---------|
| requests | HTTP client | `pip install requests` |
| httpx | Async HTTP client | `pip install httpx` |
| aiohttp | Async HTTP | `pip install aiohttp` |
| pyyaml / yaml | YAML parsing | `pip install pyyaml` |
| toml | TOML parsing | `pip install toml` |
| rich | Terminal formatting | `pip install rich` |
| click | CLI framework | `pip install click` |
| typer | CLI framework | `pip install typer` |
| python-dotenv | .env loading | `pip install python-dotenv` |
| beautifulsoup4 / bs4 | HTML parsing | `pip install beautifulsoup4` |
| lxml | XML parsing | `pip install lxml` |
| pillow / PIL | Image processing | `pip install pillow` |
| pydantic | Data validation | `pip install pydantic` |

## Heavy Packages (consider dedicated venv)

| Package | Description | Size | Install |
|---------|-------------|------|---------|
| sklearn / scikit-learn | Machine learning | ~200MB | `pip install scikit-learn` |
| pandas | Data analysis | ~100MB | `pip install pandas` |
| numpy | Numerical computing | ~50MB | `pip install numpy` |
| scipy | Scientific computing | ~150MB | `pip install scipy` |
| torch | Deep learning | ~2GB | `pip install torch` |
| tensorflow | Deep learning | ~1GB | `pip install tensorflow` |
| transformers | NLP models | ~500MB | `pip install transformers` |
| sentence-transformers | Embeddings | ~500MB | `pip install sentence-transformers` |
| playwright | Browser automation | ~200MB | `pip install playwright` |
| selenium | Browser automation | ~100MB | `pip install selenium` |
| opencv-python / cv2 | Computer vision | ~100MB | `pip install opencv-python` |
| matplotlib | Plotting | ~50MB | `pip install matplotlib` |

## Venv Recommendation Rules

- **No venv needed**: Only stdlib + common packages
- **Consider venv**: 1+ heavy package
- **Require venv**: 2+ heavy packages OR torch/tensorflow
