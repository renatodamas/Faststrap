# MapView (Experimental)

`MapView` renders an interactive Leaflet map with optional CDN asset injection.

## Import

```python
from faststrap import MapView
```

## Basic Usage

```python
MapView(
    latitude=6.5244,
    longitude=3.3792,
    zoom=12,
    popup_text="Lagos",
)
```

## Key Options

- `include_assets=True`: inject Leaflet CSS/JS from CDN (default)
- `include_assets=False`: skip injection if your app already loads Leaflet
- `marker=True`: place a marker at the center coordinate
- `popup_text="..."`: optional marker popup text

## Size Implication

Leaflet is CDN-first in this component, so Faststrap wheel size does not
increase unless you choose to vendor assets yourself.
