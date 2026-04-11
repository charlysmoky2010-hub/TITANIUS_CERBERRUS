# FIRST SKILL: LEAD RECOVERY AUDIT

## Why this is first
This is the first real skill because it is close to money.
It solves a painful, easy-to-understand problem:
people and small businesses lose revenue because leads go cold, follow-up is inconsistent, and no one knows which prospects are still worth chasing.

## Skill objective
Turn a messy lead list into a ranked recovery queue.

## Input contract
Each lead record should support these fields where available:
- `lead_id`
- `name`
- `company`
- `source`
- `status`
- `last_contact_date`
- `created_at`
- `estimated_value`
- `pipeline_stage`
- `owner`
- `email`
- `phone`
- `notes`
- `reply_count`
- `meeting_count`
- `deal_probability`

## Normalized states
The workflow should normalize raw statuses into a smaller set:
- `new`
- `contacted`
- `waiting`
- `stale`
- `qualified`
- `proposal`
- `won`
- `lost`
- `do_not_contact`

## Exclusion rules
Do not score or prioritize leads that are:
- already won
- clearly lost with final rejection
- marked do not contact
- missing all usable contact routes

## Core scoring logic
Recovery score is a weighted score from 0 to 100 based on:
- recency decay
- estimated value
- stage quality
- signal of past engagement
- source quality
- notes-based urgency or fit

### Suggested scoring dimensions
- `staleness_score`: how overdue the lead is for follow-up
- `value_score`: potential monetary value
- `engagement_score`: prior replies, meetings, signals
- `stage_score`: how close this lead was to converting
- `contactability_score`: whether there is enough data to act

## Required output fields
Each scored lead should output:
- `lead_id`
- `normalized_status`
- `recovery_score`
- `priority_band`
- `urgency`
- `recommended_action`
- `message_angle`
- `reason_summary`
- `next_follow_up_date`

## Result envelope
Every run should return a JSON envelope shaped like:

```json
{
  "engine": "LEAD_RECOVERY_AUDIT",
  "mode": "dry|apply|report",
  "status": "OK|DRY_READY|ERROR",
  "timestamp_utc": "ISO-8601",
  "input_summary": {
    "lead_count": 0,
    "excluded_count": 0,
    "scored_count": 0
  },
  "summary": {
    "high_priority_count": 0,
    "estimated_recoverable_value": 0,
    "top_actions": []
  },
  "artifacts": [],
  "recommended_next_action": "..."
}
```

## Markdown report sections
The markdown report should include:
- executive summary
- top 10 recovery opportunities
- blocked leads
- quick wins
- recommended follow-up actions
- assumptions and data gaps

## Acceptance criteria for version 1
Version 1 is good enough when it can:
1. read a JSON or CSV lead list
2. normalize statuses
3. exclude bad records
4. score remaining leads
5. rank the best recovery opportunities
6. emit JSON and markdown outputs
7. explain why each high-priority lead was selected

## Failure log rules
Every failed run should produce notes on:
- missing fields
- invalid dates
- contradictory statuses
- uncontactable leads
- scoring ambiguity

Those failures must be turned into future skill improvements instead of being forgotten like every other avoidable mess.
