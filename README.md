# TITANIUS_CERBERRUS

Turn messy prospect data into a ranked revenue recovery queue.

TITANIUS_CERBERRUS is a focused workflow product for founders, creators, consultants, agencies, and small teams that lose revenue because follow-up is inconsistent, lead lists are messy, and no one knows which opportunities are still worth chasing.

The first public workflow in this repository is **`lead_recovery_audit`**.
It reads a lead list, normalizes pipeline states, excludes dead or unusable records, scores recovery potential, and produces a prioritized action queue with JSON and Markdown outputs.

## What it does

- Ingests JSON or CSV lead data
- Normalizes raw statuses into a smaller actionable set
- Excludes won, lost, do-not-contact, and uncontactable records
- Scores remaining leads by recovery potential
- Produces a ranked queue of follow-up opportunities
- Generates structured JSON and readable Markdown reports

## Why this exists

Most small teams do not have a clean revenue recovery process.
Leads go cold, proposal-stage deals drift, and valuable contacts disappear into a spreadsheet graveyard.

This project turns that chaos into a decision-ready queue:

- which leads are still worth chasing
- why they were prioritized
- what action to take next
- when to follow up

This is not a vague "agentic platform" demo.
The public repository is intentionally centered on one real workflow that is close to money.

## Quick start

### 1. Install

```bash
python -m pip install --upgrade pip
pip install -e . pytest
```

### 2. List available workflows

```bash
python titanius_cli.py list
```

### 3. Run the demo workflow

```bash
python titanius_cli.py run lead_recovery_audit \
  --input samples/leads_demo.v1.json \
  --mode report \
  --output-json reports/lead_recovery.json \
  --output-md reports/lead_recovery.md
```

## Example outputs

A successful run returns a JSON envelope with fields such as:

- `engine`
- `mode`
- `status`
- `timestamp_utc`
- `input_summary`
- `summary`
- `top_recovery_queue`
- `markdown_report`
- `recommended_next_action`

The ranked queue includes fields such as:

- `lead_id`
- `normalized_status`
- `recovery_score`
- `priority_band`
- `urgency`
- `recommended_action`
- `message_angle`
- `reason_summary`
- `next_follow_up_date`

See:

- `samples/leads_demo.v1.json`
- `reports/lead_recovery_report.example.json`
- `docs/FIRST_SKILL_LEAD_RECOVERY.md`
- `docs/LOCAL_RUNBOOK.md`

## Who this is for

This repository is especially relevant for:

- solo founders
- creators with inbound demand
- consultants and service businesses
- agencies with stale pipelines
- small teams that need a lightweight recovery workflow before buying a large CRM stack

## Repository structure

```text
config/       scoring rules and workflow configuration
core/         shared registry and envelope helpers
docs/         product notes and local run instructions
reports/      example outputs
samples/      demo input files
tests/        workflow tests
workflows/    executable revenue workflows
titanius_cli.py
```

## Current scope

The current public scope is deliberately narrow:

- one real workflow
- one clear problem
- one repeatable output format

That is by design.
The goal is to ship useful revenue-adjacent workflows before expanding into a larger operating system.

## Project status

Early-stage, but structured for real use:

- installable Python package
- CLI entry point
- example dataset
- tests
- CI workflow
- lightweight landing page in `index.html`

## Roadmap

Short-term direction:

1. strengthen report quality and message suggestions
2. support more CSV variations and messier real-world inputs
3. add adjacent revenue workflows after lead recovery is stable
4. improve examples, screenshots, and buyer-facing proof

## Positioning

If you are here looking for a giant autonomous everything-machine, this is not that repository.
This public repo is the clean storefront for practical, revenue-near workflows.
The first one is lead recovery.

That focus is the point.
