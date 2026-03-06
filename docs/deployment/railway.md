# Deploying to Railway

Railway runs your app as a persistent process. It is recommended for SSE, WebSockets, background workers, and in-memory process state. `use_cdn=False` (default) works correctly.

## Project Structure

```text
my-app/
|-- main.py
|-- requirements.txt
`-- railway.toml
```

## main.py

```python
from fasthtml.common import FastHTML
from faststrap import add_bootstrap

app = FastHTML()
add_bootstrap(app)  # use_cdn=False is fine on Railway

# Expose bare app; Railway uses startCommand
```

## railway.toml

```toml
[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
```

## Deploy

```bash
npm i -g @railway/cli
railway login
railway init
railway up
```

Set variables with `railway variables set DATABASE_URL=...`.

## SSE on Railway

SSE works with default Railway process hosting. Only add Nginx buffering directives if you place Nginx in front.
