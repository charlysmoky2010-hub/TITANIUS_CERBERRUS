# TITANIUS Web Missing Items

This backlog tracks the remaining web work. Humanity has somehow survived without a canonical website backlog until now, but we are correcting that tragedy.

## Priority 0: Structure

- [x] Create `/web` root contract.
- [x] Create canonical page registry.
- [x] Assign TITANIUS_WEB_STEWARD as web owner.
- [ ] Import the current ready-looking website source into `web/pages/home`.
- [ ] Decide the public deployment target: GitHub Pages, Vercel, Netlify, or custom host.

## Priority 1: Public pages

- [ ] Home page: clear headline, offer, CTA, project boundary.
- [ ] About page: explain TITANIUS/CERBERRUS144 without overpromising.
- [ ] Crypto paper dashboard page: read-only only, no exchange execution.
- [ ] Contact page: add approved public contact address only after confirmation.
- [ ] Legal/safety note: paper trading, no financial advice, no private-key handling.

## Priority 2: Assets

- [ ] Add hero image source under `web/assets/hero/`.
- [ ] Add favicon and social preview image.
- [ ] Add brand tokens: typography, spacing, core colors.
- [ ] Add image attribution/source notes where required.

## Priority 3: Engineering checks

- [ ] Add web hygiene workflow.
- [ ] Add no-secret scan for web files.
- [ ] Add registry validation.
- [ ] Add page status report artifact.

## Priority 4: Content quality

- [ ] Remove vague AI hype language.
- [ ] Keep claims grounded and auditable.
- [ ] Make every CTA point to an actual next action.
- [ ] Keep crypto content read-only until ledger verification is clean.

## Current next action

Import the existing website source into `web/pages/home`, then update `web/registry/titanius-web-pages.json` from `needs_source_import` to `draft_ready`.
