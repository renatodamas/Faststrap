# FilterBar

Composable filter layout with HTMX integration and optional “Apply” mode.

---

## Quick Start

```python
from faststrap import FilterBar, MultiSelect, RangeSlider

FilterBar(
    MultiSelect("team", ("ops", "Ops"), ("data", "Data")),
    RangeSlider("score", min_value=0, max_value=100),
    mode="apply",
)
```

---

## API Reference

::: faststrap.components.forms.filter_bar.FilterBar
    options:
        show_source: true
        heading_level: 4
