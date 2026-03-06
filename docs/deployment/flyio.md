# Deploying to Fly.io

Fly.io runs your app in persistent containers across global regions. It is a strong choice for production SSE workloads.

## Dockerfile

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

## fly.toml (key sections)

```toml
[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = false
  auto_start_machines = true
```

## Deploy

```bash
fly launch
fly deploy
```

## SSE Note

Set `auto_stop_machines = false` for SSE. Stopped machines will drop active streaming connections.

If you front Fly.io with Nginx, use this SSE proxy block:

```nginx
location /api/stream {
    proxy_pass http://127.0.0.1:5001;
    proxy_buffering off;
    proxy_cache off;
    proxy_set_header Connection '';
    proxy_http_version 1.1;
    chunked_transfer_encoding on;
}
```
