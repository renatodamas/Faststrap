# OptimisticAction

`OptimisticAction` is a button preset for optimistic UI flows where the UI updates
immediately, then either commits or rolls back based on the server response.

## Import

```python
from faststrap.presets import OptimisticAction
```

## Basic Usage

```python
OptimisticAction(
    "Archive",
    endpoint="/items/42/archive",
    target="#item-42",
    action_id="archive-42",
    payload={"item_id": 42},
    variant="warning",
)
```

## Event Contract

`OptimisticAction` dispatches bubbling `CustomEvent`s from the button:

- `faststrap:optimistic:apply` before request starts
- `faststrap:optimistic:commit` after successful response
- `faststrap:optimistic:rollback` when request fails

Event `detail` includes:

- `actionId`
- `endpoint`
- `method`
- `target`
- `payload`
- `reason`

## Server Contract Recommendation

Use idempotent endpoints and return consistent error status codes for failed writes.
Client listeners should:

1. Apply temporary UI state on `apply`
2. Finalize UI state on `commit`
3. Restore previous UI state on `rollback`

## Notes

- Supported methods: `get`, `post`, `put`, `patch`, `delete`
- Unsupported methods raise `ValueError`
- Designed as an interaction preset; no Faststrap core API changes required
