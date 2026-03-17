# DashboardGrid

Responsive grid layout for dashboards with consistent spacing and card sizing.

---

## Quick Start

```python
from faststrap import DashboardGrid, StatCard

DashboardGrid(
    StatCard("Revenue", "$12k"),
    StatCard("Users", "2,410"),
    cols=3,
    gap=1.5,
)
```

---

## API Reference

::: faststrap.components.layout.dashboard_grid.DashboardGrid
    options:
        show_source: true
        heading_level: 4
