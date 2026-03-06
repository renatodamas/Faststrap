# Deploying to Render

Render runs your app as a persistent web service and supports SSE/WebSocket workloads. The free web service tier sleeps when idle.

## Project Structure

```text
my-app/
|-- main.py
|-- requirements.txt
`-- render.yaml
```

## main.py

```python
from fasthtml.common import FastHTML
from faststrap import add_bootstrap

app = FastHTML()
add_bootstrap(app)  # Local static serving is supported on Render
```

## render.yaml (optional IaC)

```yaml
services:
  - type: web
    name: faststrap-app
    env: python
    plan: starter
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
```

## Manual Setup

1. Create a new Web Service in Render.
2. Connect repository.
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## Notes

- Free tier sleeps after inactivity; wake-up introduces latency.
- Upgrade plan to keep service always-on for real-time workloads.
