# MultiSelect

Bootstrap multi-select built for FastHTML.

---

## Quick Start

```python
from faststrap import MultiSelect

MultiSelect(
    "team",
    ("platform", "Platform"),
    ("ops", "Ops"),
    ("data", "Data"),
    selected=["data"],
    label="Teams",
)
```

---

## API Reference

::: faststrap.components.forms.multi_select.MultiSelect
    options:
        show_source: true
        heading_level: 4
