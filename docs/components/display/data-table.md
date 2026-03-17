# DataTable

`DataTable` is a higher-level table with built-in sorting, search, and pagination. It accepts `list[dict]` and pandas/polars DataFrames.

---

## Quick Start

```python
from faststrap import DataTable

DataTable(
    data,
    sortable=True,
    searchable=True,
    pagination=True,
    per_page=25,
)
```

---

## Server-Side Contract

When you pass an `endpoint`, DataTable emits these query params:

- `sort`
- `direction`
- `page`
- `per_page`
- `q` (or your `search_param`)
- any `filters` you provide

```python
DataTable(
    data,
    endpoint="/users",
    sortable=True,
    searchable=True,
    pagination=True,
)
```

---

## Export Integration

Use the helper to reuse the table query state for exports:

```python
from faststrap import DataTable, ExportButton

params = DataTable.export_params(
    sort="name",
    direction="asc",
    search="alice",
    filters={"team": "ops"},
)

ExportButton("Export CSV", endpoint="/export", export_format="csv", extra_params=params)
```

---

## API Reference

::: faststrap.components.display.data_table.DataTable
    options:
        show_source: true
        heading_level: 4
