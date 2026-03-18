# NIS patterns

Use `C:\Users\Meshell\Desktop\FastHTML\NIS` as the primary real-world reference for how the user combines FastHTML with Faststrap in production-style apps.

## Read first

- `NIS/main.py`
- `NIS/app/presentation/components/shared/theme.py`
- `NIS/app/presentation/components/ui/layout.py`
- `NIS/app/presentation/routes/landing.py`
- `NIS/app/presentation/routes/auth.py`
- `NIS/app/presentation/assets/css/custom.css`

## Patterns to copy

### App bootstrap

From `NIS/main.py`:

- create `FastHTML(...)` with real app settings
- call `add_bootstrap(app, theme=..., mode=...)`
- call a shared function that sets component defaults
- mount project assets with `mount_assets(...)`
- append project CSS after Faststrap so app-specific polish is easy to control

### Theme structure

From `theme.py`:

- keep brand colors in one shared module
- use `create_theme(...)` for the brand system
- use `set_component_defaults(...)` for consistent app-wide component behavior
- expose color constants for custom layout pieces

### Layout structure

From `layout.py`:

- create dedicated layout helpers for recurring shells such as dashboard, auth, or landing
- keep navigation/layout composition outside page business logic
- use responsive structural wrappers and shared CSS classes for polish

### Presentation architecture

From `routes/`:

- organize routes by area or role
- keep reusable fragments in components modules
- use route setup functions like `setup_*_routes(app)` for modular composition

### Design language

From `landing.py` and `custom.css`:

- combine Faststrap sections/components with custom CSS classes
- layer imagery, overlays, gradients, glassmorphism, and floating cards deliberately
- use typography, spacing, and visual contrast to create hierarchy
- make CTAs obvious and section transitions intentional

## What this means for future builds

When the user asks for a company site, portal, or dashboard with Faststrap:

- do not stop at default component composition
- create a shared theme module
- create shared layouts
- add custom CSS that pushes the design beyond stock Bootstrap
- use the page structure and separation of concerns seen in NIS

