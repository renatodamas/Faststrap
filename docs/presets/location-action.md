# LocationAction

`LocationAction` is a progressive helper for browser geolocation flows.

## Import

```python
from faststrap.presets import LocationAction
```

## Usage

```python
LocationAction(
    "Use my location",
    endpoint="/api/location",
    target="#location-result",
)
```

## Event Contract

- `faststrap:location:success`
- `faststrap:location:error`

Both events bubble and include structured `detail` payloads.

## Privacy Notes

- Always request location in direct response to user interaction.
- Provide a clear non-location fallback in your UI.
- Treat coordinates as sensitive data and avoid long-term storage by default.
