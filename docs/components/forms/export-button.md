# ExportButton

Standardized export action for CSV/Excel/JSON/PDF downloads.

---

## Quick Start

```python
from faststrap import ExportButton

ExportButton("Export CSV", endpoint="/export", export_format="csv")
```

---

## With DataTable State

```python
params = DataTable.export_params(sort="name", direction="asc", search="alice")
ExportButton("Export", endpoint="/export", extra_params=params)
```

---

## API Reference

::: faststrap.components.forms.export_button.ExportButton
    options:
        show_source: true
        heading_level: 4
