"""Tests for PWA module."""

from fasthtml.common import FastHTML
from starlette.testclient import TestClient

from faststrap.pwa import PwaMeta, add_pwa


def test_pwa_meta_generation():
    """Test PwaMeta component generates correct tags."""
    tags = PwaMeta(name="Test App", theme_color="#000000", icon_path="/icon.png")

    # Check for essential tags
    assert any(
        t.tag == "meta"
        and t.attrs.get("name") == "theme-color"
        and t.attrs.get("content") == "#000000"
        for t in tags
    )
    assert any(t.tag == "link" and t.attrs.get("rel") == "manifest" for t in tags)
    assert any(t.tag == "link" and t.attrs.get("rel") == "apple-touch-icon" for t in tags)
    viewport = next(t for t in tags if t.tag == "meta" and t.attrs.get("name") == "viewport")
    assert viewport.attrs.get("content") == "width=device-width, initial-scale=1"


def test_add_pwa_injection():
    """Test add_pwa injects headers and routes."""
    app = FastHTML()

    add_pwa(app, name="My PWA", service_worker=True, offline_page=True)

    # Check headers injected
    assert len(app.hdrs) > 0
    # Check for service worker registration script
    assert any(h.tag == "script" and "navigator.serviceWorker.register" in str(h) for h in app.hdrs)

    # Check routes added
    route_paths = [r.path for r in app.routes]
    assert "/manifest.json" in route_paths
    assert "/sw.js" in route_paths
    assert "/offline" in route_paths


def test_add_pwa_no_sw():
    """Test add_pwa with service_worker=False."""
    app = FastHTML()

    add_pwa(app, service_worker=False)

    route_paths = [r.path for r in app.routes]
    assert "/manifest.json" in route_paths
    assert "/sw.js" not in route_paths


def test_manifest_route_returns_json():
    """Manifest route should return JSON payload directly."""
    app = FastHTML()
    add_pwa(app, name="My PWA")

    client = TestClient(app)
    response = client.get("/manifest.json")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    payload = response.json()
    assert payload["name"] == "My PWA"
    assert payload["start_url"] == "/"


def test_service_worker_route_returns_javascript():
    """Service worker route should return JS file without response double-wrapping."""
    app = FastHTML()
    add_pwa(app, service_worker=True)

    client = TestClient(app)
    response = client.get("/sw.js")

    assert response.status_code == 200
    assert "application/javascript" in response.headers["content-type"]
    assert "self.addEventListener" in response.text


def test_service_worker_uses_hardened_precache_and_runtime_caching():
    """Default service worker should be resilient and include runtime caching strategies."""
    app = FastHTML()
    add_pwa(app, service_worker=True)

    client = TestClient(app)
    response = client.get("/sw.js")

    assert response.status_code == 200
    sw = response.text
    assert "Promise.allSettled(PRECACHE_URLS.map((url) => cache.add(url)))" in sw
    assert "cache.put(request, response.clone())" in sw
    assert 'if (event.request.mode === "navigate")' in sw
    assert "staleWhileRevalidate(event.request)" in sw


def test_service_worker_accepts_cache_and_precache_configuration():
    """Service worker should reflect optional cache naming and additional precache URLs."""
    app = FastHTML()
    add_pwa(
        app,
        service_worker=True,
        cache_name="myapp-cache",
        cache_version="v2026-02-23",
        pre_cache_urls=("/health", "/assets/logo.png"),
    )

    client = TestClient(app)
    response = client.get("/sw.js")

    assert response.status_code == 200
    sw = response.text
    assert 'const CACHE_NAME = "myapp-cache-v2026-02-23";' in sw
    assert '"/health"' in sw
    assert '"/assets/logo.png"' in sw


def test_add_pwa_scope_uses_scoped_routes_and_registration():
    """Scope should drive manifest/sw/offline paths and registration script."""
    app = FastHTML()
    add_pwa(app, scope="/myapp/")

    route_paths = [r.path for r in app.routes]
    assert "/myapp/manifest.json" in route_paths
    assert "/myapp/sw.js" in route_paths
    assert "/myapp/offline" in route_paths

    script_text = "".join(str(h) for h in app.hdrs if getattr(h, "tag", "") == "script")
    assert "register('/myapp/sw.js'" in script_text
    assert "scope: '/myapp/'" in script_text


def test_background_sync_foundation_disabled_by_default():
    """Service worker should keep background sync disabled unless explicitly enabled."""
    app = FastHTML()
    add_pwa(app, service_worker=True)

    client = TestClient(app)
    response = client.get("/sw.js")
    assert response.status_code == 200
    sw = response.text
    assert "const ENABLE_BACKGROUND_SYNC = false" in sw
    assert "BACKGROUND_SYNC_TAG" in sw


def test_background_sync_foundation_enabled_with_custom_tag():
    """Background sync scaffold should be present when enabled."""
    app = FastHTML()
    add_pwa(
        app,
        service_worker=True,
        enable_background_sync=True,
        background_sync_tag="faststrap-sync-queue",
    )

    client = TestClient(app)
    response = client.get("/sw.js")
    assert response.status_code == 200
    sw = response.text
    assert "const ENABLE_BACKGROUND_SYNC = true" in sw
    assert 'const BACKGROUND_SYNC_TAG = "faststrap-sync-queue";' in sw
    assert 'self.addEventListener("sync"' in sw

    script_text = "".join(str(h) for h in app.hdrs if getattr(h, "tag", "") == "script")
    assert "reg.sync.register('faststrap-sync-queue')" in script_text


def test_pwa_route_cache_policies_are_embedded_in_sw():
    """Route strategy map should be serialized into the SW for policy dispatch."""
    app = FastHTML()
    add_pwa(
        app,
        service_worker=True,
        route_cache_policies={
            "/api/public/": "stale-while-revalidate",
            "/assets/": "cache-first",
        },
    )

    client = TestClient(app)
    response = client.get("/sw.js")
    assert response.status_code == 200
    sw = response.text
    assert (
        'const ROUTE_CACHE_POLICIES = {"/api/public/": "stale-while-revalidate", "/assets/": "cache-first"};'
        in sw
    )
    assert "resolveRouteStrategy(event.request)" in sw
    assert 'if (routeStrategy === "cache-first")' in sw


def test_pwa_push_foundation_enabled():
    """Push handlers should only be active when explicitly enabled."""
    app = FastHTML()
    add_pwa(app, service_worker=True, enable_push=True, default_push_title="My App Notice")

    client = TestClient(app)
    response = client.get("/sw.js")
    assert response.status_code == 200
    sw = response.text
    assert "const ENABLE_PUSH = true" in sw
    assert 'const DEFAULT_PUSH_TITLE = "My App Notice";' in sw
    assert 'self.addEventListener("push"' in sw
    assert 'self.addEventListener("notificationclick"' in sw
