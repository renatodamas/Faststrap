# FormBuilder.from_pydantic (Beta)

`FormBuilder.from_pydantic()` generates a Bootstrap-styled form from a Pydantic model.

!!! info "Naming update in v0.6.1"
    Starting in Faststrap `v0.6.1`, the preferred import is `FormBuilder` to avoid confusion
    with FastHTML's native `Form` element.

    - `v0.6.1+`: `from faststrap import FormBuilder`
    - `v0.6.0 and earlier`: `from faststrap import Form`
    - `Form` remains available as a compatibility alias, but new code should prefer `FormBuilder`.

## Import

```python
from faststrap import FormBuilder
```

## Basic Usage

```python
from pydantic import BaseModel, EmailStr

class Signup(BaseModel):
    email: EmailStr
    age: int
    marketing_opt_in: bool = False

form = FormBuilder.from_pydantic(Signup, action="/signup")
```

## Supported Field Mapping (MVP)

- `str` -> text input
- `EmailStr` -> email input
- `int` -> number input
- `float` -> number input (`step="any"`)
- `bool` -> checkbox
- `Literal[...]` -> select
- `Enum` -> select

## Options

- `include=[...]` include only selected fields
- `exclude=[...]` remove selected fields
- `submit_label="Submit"` customize button text
- `submit_variant="primary"` customize button style

## Backward Compatibility

If you are maintaining a project pinned below `v0.6.1`, this older import still works:

```python
from faststrap import Form

form = Form.from_pydantic(Signup, action="/signup")
```
