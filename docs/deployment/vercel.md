# Deploying to Vercel

## Prerequisites

- Stateless app (no SSE, WebSockets, background workers, in-memory state)
- `use_cdn=True` in `add_bootstrap()` (required: no writable local static hosting)
- Python 3.10+

## Project Structure

```text
my-app/
|-- main.py
|-- requirements.txt
`-- vercel.json
```

## Step 1 - Configure main.py

```python
from fasthtml.common import FastHTML
from faststrap import add_bootstrap, Card, Button, Input

app = FastHTML()
add_bootstrap(app, use_cdn=True, include_favicon=False)

@app.route("/")
def home():
    return Card(
        Input("email", input_type="email", label="Email", required=True),
        Button("Sign In", variant="primary", cls="w-100", hx_post="/login"),
        header="Welcome back",
    )

# Correct: expose bare app object
# Wrong: do not call serve() in serverless entrypoint
```

## Step 2 - requirements.txt

```text
python-fasthtml
faststrap
```

## Step 3 - vercel.json

```json
{
  "builds": [{"src": "main.py", "use": "@vercel/python"}],
  "routes": [{"src": "/(.*)", "dest": "main.py"}]
}
```

## Step 4 - Deploy

```bash
npm i -g vercel
vercel
```

Set env vars as needed, for example: `vercel env add DATABASE_URL`.

## Connecting to an External Backend

```python
Button(
    "Save",
    hx_post="https://api.yourapp.com/save",
    hx_target="#result",
)
```

Backend CORS must expose HTMX headers:

```python
expose_headers=[
    "HX-Location", "HX-Redirect", "HX-Refresh",
    "HX-Trigger", "HX-Reswap", "HX-Retarget",
]
```

Without `expose_headers`, preset response helpers such as `toast_response()` and `hx_redirect()` fail cross-origin.

## What Does Not Work on Vercel

- SSE (Server-Sent Events)
- WebSockets
- Background workers
- In-memory state between requests
- Filesystem writes

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| 404 on Bootstrap CSS/JS or icons | `use_cdn=True` not set | Add `use_cdn=True` to `add_bootstrap()` |
| App works locally, 500 on Vercel | `serve()` called in main.py | Remove `serve()` call |
| HTMX response helpers not working cross-origin | Missing `expose_headers` | Add all `HX-*` headers to backend CORS `expose_headers` |
| Cold start delay | Serverless cold starts | Expected; reduced on paid plans |
