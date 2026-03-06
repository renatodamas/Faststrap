# Faststrap v0.5.9 Plan (Pre-v0.6.0)

Target release window: March 2026

## Objectives

1. Ship high-value pre-v0.6.0 features without breaking API stability.
2. Keep optional integrations out of core dependency/runtime weight.
3. Validate data-adjacent MVPs before v0.6.0 expands scope.

## Scope

1. MapView (Leaflet, experimental, CDN-first, optional)
2. Form.from_pydantic() MVP (beta)
3. Table.from_df() MVP (beta, static render first)
4. Hardening of:
   - OptimisticAction
   - Markdown renderer
   - LocationAction
   - PWA background sync/push/route cache foundations

## Constraints

1. No breaking public API changes unless unavoidable.
2. Any new dependency must be optional.
3. Keep `ruff`, `black --check`, `mypy`, and `pytest` green.

## Release Checklist

1. API docs + examples added for every new public surface.
2. Changelog and roadmap updated.
3. Full quality gate pass in CI.
4. Migration notes for any behavior changes.
