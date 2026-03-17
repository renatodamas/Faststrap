# SSETarget

`SSETarget` connects a DOM container to an SSE endpoint and updates it as events arrive.

---

## Quick Start

```python
from faststrap import SSETarget

SSETarget(
    "Waiting for updates...",
    endpoint="/api/stream",
    swap="inner",
)
```

---

## Pair With SSEStream

```python
from faststrap.presets import SSEStream, sse_event

@app.get("/api/stream")
async def stream():
    async def gen():
        yield sse_event("Hello")
    return SSEStream(gen())
```

---

## API Reference

::: faststrap.components.display.sse_target.SSETarget
    options:
        show_source: true
        heading_level: 4
