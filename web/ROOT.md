# TITANIUS Web Root

This directory is the canonical root for public-facing web work in the TITANIUS ecosystem.

TITANIUS_WEB_STEWARD is responsible for keeping website structure, page registry, missing-item backlog, and deployment readiness visible and auditable.

## Current mandate

1. Treat `/web` as the source-of-truth web layer.
2. Keep page ownership documented before adding new surfaces.
3. Track missing website parts in `web/backlog/missing-items.md`.
4. Keep generated assets separate from source pages.
5. Never mix wallet secrets, private keys, tokens, or personal data into web files.

## Root map

- `web/ROOT.md`: this root contract.
- `web/registry/titanius-web-pages.json`: canonical page registry.
- `web/backlog/missing-items.md`: next missing work.
- `agents/TITANIUS_WEB_STEWARD.md`: agent responsibility charter.
- `.github/workflows/titanius-web-steward.yml`: lightweight GitHub web hygiene check.

## Steward rule

No public page becomes canonical unless it has a registry entry, clear status, and a next action.
