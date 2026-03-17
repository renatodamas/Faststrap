# Chart

`Chart` renders Matplotlib, Plotly, Altair, or raw SVG/HTML outputs in a single component.

---

## Quick Start

```python
from faststrap import Chart

Chart(fig, backend="matplotlib")
```

---

## Plotly / Altair

```python
Chart(fig, backend="plotly", include_js=True)
```

---

## Raw SVG/HTML (Explicit)

```python
Chart("<svg>...</svg>", backend="svg", allow_unsafe_html=True)
```

---

## API Reference

::: faststrap.components.display.chart.Chart
    options:
        show_source: true
        heading_level: 4
