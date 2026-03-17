# SSEStream

`SSEStream` builds a `text/event-stream` response for Server‑Sent Events.

---

## Quick Start

```python
from faststrap.presets import SSEStream, sse_event

@app.get("/api/stream")
async def stream():
    async def gen():
        yield sse_event("Hello")
    return SSEStream(gen())
```

You can also emit keep‑alive comments:

```python
from faststrap.presets import sse_comment

yield sse_comment("keepalive")
```

---

## API Reference

::: faststrap.presets.streams.SSEStream
    options:
        show_source: true
        heading_level: 4
