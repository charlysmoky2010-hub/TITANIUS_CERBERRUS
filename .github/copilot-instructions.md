# TITANIUS_CERBERRUS Copilot Instructions

## Product intent
TITANIUS_CERBERRUS is not a generic AI playground. It is a revenue-focused orchestration core for building small, sharp, monetizable workflow products.

The first commercial wedge is:
- lead recovery for solo founders and small businesses
- creator offer validation and lightweight business intelligence
- modular automation that produces terminal-friendly JSON reports

## Engineering principles
- Python-first repository
- typed code where practical
- CLI-first user experience
- JSON output by default for automation and reporting
- dry-run and smoke-test modes before destructive or live execution
- small composable modules instead of giant files
- minimal dependencies
- explicit config over hidden magic

## Preferred structure
- `core/` for orchestration primitives
- `agents/` for domain-specific agents
- `workflows/` for executable flows
- `runtime/` for generated state and temporary runtime data
- `reports/` for JSON and markdown reports
- `config/` for policy and product configuration
- `docs/` for strategy and architecture
- `tests/` for smoke tests and unit tests

## First build target
Build a lightweight orchestration MVP with:
1. a registry that can load and list modules
2. a CLI entrypoint
3. a dry-run command
4. a smoke-test command
5. one demo revenue workflow such as lead recovery scoring or offer validation scoring
6. JSON result envelopes with timestamps, status, workflow name, and recommended next action

## Output contract
Every executable workflow should return a JSON object with a shape similar to:
```json
{
  "engine": "NAME",
  "mode": "dry|apply|report",
  "status": "OK|DRY_READY|ERROR",
  "timestamp_utc": "ISO-8601",
  "summary": {},
  "artifacts": [],
  "recommended_next_action": "..."
}
```

## Commercial bias
Prefer features that support a fast path to first revenue:
- lead intake
- lead qualification
- follow-up recovery
- offer scoring
- creator niche analysis
- small-business operational automation

Avoid spending time on:
- abstract agent swarms with no buyer
- premature distributed systems
- complicated UI before a working command-line product
- infrastructure complexity without a customer problem

## Documentation standard
When generating docs, explain:
- who pays
- what problem is solved
- what the smallest sellable workflow is
- what inputs and outputs the workflow uses
- how success is measured

## Code quality
Keep code readable, boring, testable, and easy to extend. Prefer simple functions and small classes. Name modules clearly. Build foundations that can become products, not demos that look clever and do nothing.
