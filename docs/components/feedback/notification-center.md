# NotificationCenter

Dropdown notification hub built on Bootstrap dropdowns.

---

## Quick Start

```python
from faststrap import NotificationCenter

NotificationCenter(
    ("New report ready", "/reports/1"),
    ("Server maintenance", "/status"),
    count=2,
)
```

---

## API Reference

::: faststrap.components.feedback.notification_center.NotificationCenter
    options:
        show_source: true
        heading_level: 4
