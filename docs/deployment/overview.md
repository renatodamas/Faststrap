# Deploying Faststrap Apps

Faststrap apps are FastHTML/ASGI applications. The right deployment platform depends on whether your app needs persistent features such as SSE, WebSockets, background workers, or in-memory process state.

## Decision Flow

```text
Does your app need SSE, WebSockets, or background workers?
|
|-- YES -> Railway (easiest) · Fly.io (production) · VPS (full control)
|
`-- NO -- Is your app completely stateless?
          (reads from external DB only, no in-memory dicts)
          |
          |-- YES -> Vercel (recommended) · Cloud Run · AWS Lambda
          |
          `-- NO --> Railway · Render · Fly.io
```

## Platform Comparison

| Platform | Type | SSE | Free Tier | Best For |
|---|---|---|---|---|
| Vercel | Serverless | No | Yes (Generous) | Stateless apps |
| Railway | PaaS | Yes | Yes ($5 credit) | Easiest deploy, beginners |
| Render | PaaS | Yes | Yes (sleeps) | Production, free tier caveats |
| Fly.io | PaaS/Container | Yes | Yes (Generous) | Production + SSE, global |
| Koyeb | PaaS | Yes | Yes (No sleep) | Always-on free tier |
| Google Cloud Run | Serverless container | Limited | Yes (2M req/mo) | GCP ecosystem |
| AWS Lambda | Serverless | No | Yes (1M req/mo) | AWS ecosystem |
| Hetzner VPS | Infrastructure | Yes | No (€3.29/mo) | Full control, best price/perf |

## Cloudflare Compatibility

- Cloudflare Pages: No (JS/TS only)
- Cloudflare Workers: No (V8 isolates; Python ASGI apps are not viable here)
- Cloudflare Tunnel: Yes (front any VPS, free, full SSE support)
- Cloudflare CDN/Proxy: Yes (in front of any hosted server)

!!! warning "Serverless requirements"
    Serverless platforms (Vercel, AWS Lambda, Cloud Run) require:

    1. `add_bootstrap(app, use_cdn=True)` - no local static files
    2. Do **not** call `serve()` - expose the bare `app` object
    3. App must be stateless - no in-memory dicts, no file writes
    4. SSE and WebSockets are not supported on serverless
