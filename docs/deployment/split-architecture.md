# Split Architecture: UI on Vercel + Backend on Render

```text
User -> Vercel (FastHTML + Faststrap, stateless, use_cdn=True)
           |
           | hx_post="https://api.yourapp.com/..."
           v
    Render / Railway (FastAPI backend, persistent)
           |
           |-- PostgreSQL (Supabase / Render DB)
           |-- SSE endpoints
           `-- Background workers
```

## Frontend (Vercel) - main.py

```python
from fasthtml.common import *
from faststrap import add_bootstrap, Container, Input, Div

add_bootstrap(app, use_cdn=True)

@app.route("/")
def home():
    return Container(
        Input(
            "search",
            placeholder="Search...",
            hx_get="https://api.yourapp.com/search",
            hx_target="#results",
            hx_trigger="keyup changed delay:500ms",
        ),
        Div(id="results"),
    )
```

## Backend (Render/Railway) - FastAPI CORS

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourapp.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=[
        "HX-Location", "HX-Redirect", "HX-Refresh",
        "HX-Trigger", "HX-Reswap", "HX-Retarget",
    ],
)
```

!!! warning "HX-* headers must be explicitly exposed"
    CORS blocks custom response headers by default. Without `expose_headers`,
    Faststrap preset response helpers (`toast_response()`, `hx_redirect()`, etc.)
    silently fail cross-origin.

## Database Options

| Option | Cost | Best For |
|---|---|---|
| Supabase | Free tier | Easy setup, HTTP API |
| Render PostgreSQL | Free tier | Already on Render |
| Neon | Free tier | PostgreSQL, serverless-native |
