# Building PWAs with Faststrap

Faststrap provides a production-safe PWA baseline through `add_pwa()`:

- Manifest generation (`/manifest.json`)
- Service worker route (`/sw.js`)
- Automatic service worker registration
- Offline fallback route (`/offline`)
- Runtime caching for better resilience

Accessibility note:
- Faststrap keeps mobile zoom enabled by default (`width=device-width, initial-scale=1`).

## Quick Start

```python
from fasthtml.common import FastHTML
from faststrap import add_bootstrap, add_pwa

app = FastHTML()
add_bootstrap(app)

add_pwa(
    app,
    name="My App",
    short_name="MyApp",
    theme_color="#0d6efd",
    icon_path="/static/icon.png",
)
```

## What `add_pwa()` Configures

1. Injects required PWA/mobile meta tags.
2. Serves a generated `manifest.json`.
3. Serves a robust service worker script at `/sw.js`.
4. Injects service worker registration code into app headers.
5. Serves `/offline` page (enabled by default).
6. Respects `scope` for scoped deployments (for example `/myapp/sw.js`).

## Default Offline/Caching Strategy

The built-in service worker uses:

- Install: tolerant pre-cache (`Promise.allSettled`) so one failed URL does not break install.
- Navigation requests: network-first with cache fallback, then `/offline`.
- Static assets (`css`, `js`, `images`, fonts): stale-while-revalidate.
- Other GET requests: network-first with runtime cache write-through.

This is a practical baseline for production apps that need reliable offline fallback behavior.

## Advanced Configuration

`add_pwa()` now supports cache controls:

```python
add_pwa(
    app,
    cache_name="myapp-cache",
    cache_version="v2026-02-23",
    pre_cache_urls=(
        "/health",
        "/assets/logo.png",
    ),
)
```

- `cache_name`: prefix for cache storage
- `cache_version`: version suffix for cache invalidation on deploy
- `pre_cache_urls`: additional URLs to pre-cache

Faststrap still pre-caches its core defaults and `/offline`.

## Background Sync Foundation (Opt-in)

Faststrap includes a lightweight background sync scaffold that you can enable
without committing to a queue implementation yet:

```python
add_pwa(
    app,
    enable_background_sync=True,
    background_sync_tag="faststrap-background-sync",
)
```

- `enable_background_sync`: enables service worker `sync` event hooks
- `background_sync_tag`: tag used when registering sync tasks

This is intentionally a foundation layer for v0.6.x work; request queue
persistence/replay is still application-defined.

## Route-Aware Cache Policies (Opt-in)

You can define route prefix policies in the generated service worker:

```python
add_pwa(
    app,
    route_cache_policies={
        "/api/public/": "stale-while-revalidate",
        "/assets/": "cache-first",
    },
)
```

Supported strategies:

- `network-first`
- `stale-while-revalidate`
- `cache-first`

## Push Foundation (Opt-in)

Enable push event scaffolding in the generated service worker:

```python
add_pwa(
    app,
    enable_push=True,
    default_push_title="My App Notification",
)
```

This adds `push` and `notificationclick` handlers with safe defaults.

## When to Use a Custom Service Worker

Use a custom `sw.js` when you need:

- fine-grained API caching rules
- background sync
- push notifications
- per-route cache policies

In that case:

1. pass `service_worker=False` to `add_pwa()`
2. mount your own `/sw.js` route

## Mobile Components

Faststrap also includes mobile-oriented UI components:

- `BottomNav`, `BottomNavItem`
- `Sheet`
- `InstallPrompt`
