from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

from core.envelope import result_envelope

ENGINE_NAME = "LEAD_RECOVERY_AUDIT"


@dataclass
class LeadScore:
    lead_id: str
    normalized_status: str
    recovery_score: int
    priority_band: str
    urgency: str
    recommended_action: str
    message_angle: str
    reason_summary: str
    next_follow_up_date: str
    estimated_value: float


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.strptime(value[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def _load_json(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("JSON input must be a list of lead records.")
    return [dict(item) for item in data]


def _load_csv(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def load_leads(path: str) -> list[dict[str, Any]]:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    if file_path.suffix.lower() == ".json":
        return _load_json(file_path)
    if file_path.suffix.lower() == ".csv":
        return _load_csv(file_path)
    raise ValueError("Supported input formats are .json and .csv")


def load_policy(path: str = "config/lead_recovery_scoring.v1.json") -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def normalize_status(raw_status: str | None, policy: dict[str, Any]) -> str:
    mapping = policy.get("status_normalization", {})
    key = (raw_status or "").strip().lower()
    return mapping.get(key, "stale" if key else "new")


def _priority_band(score: int, policy: dict[str, Any]) -> str:
    bands = policy.get("priority_bands", {})
    for band_name, band_config in bands.items():
        if band_config["min"] <= score <= band_config["max"]:
            return band_name
    return "P4"


def _urgency_from_band(band: str) -> str:
    return {
        "P1": "high",
        "P2": "medium",
        "P3": "medium",
        "P4": "low",
    }.get(band, "low")


def _message_angle(normalized_status: str, contactability_score: int) -> str:
    if contactability_score == 0:
        return "data_gap_review"
    if normalized_status == "proposal":
        return "proposal_nudge"
    if normalized_status == "qualified":
        return "qualified_revival"
    return "value_reactivation"


def _score_lead(record: dict[str, Any], policy: dict[str, Any], today: date) -> LeadScore | None:
    normalized_status = normalize_status(record.get("status"), policy)
    if normalized_status in set(policy.get("exclusions", [])):
        return None

    has_contact_route = bool((record.get("email") or "").strip() or (record.get("phone") or "").strip())
    if not has_contact_route:
        return None

    last_contact_date = _parse_date(record.get("last_contact_date"))
    days_since_contact = (today - last_contact_date).days if last_contact_date else 999

    estimated_value = float(record.get("estimated_value") or 0)
    reply_count = int(float(record.get("reply_count") or 0))
    meeting_count = int(float(record.get("meeting_count") or 0))
    deal_probability = float(record.get("deal_probability") or 0)

    if days_since_contact >= 60:
        staleness_score = 100
    elif days_since_contact >= 30:
        staleness_score = 80
    elif days_since_contact >= 14:
        staleness_score = 55
    else:
        staleness_score = 20

    if estimated_value >= 3000:
        value_score = 100
    elif estimated_value >= 1500:
        value_score = 75
    elif estimated_value >= 750:
        value_score = 50
    else:
        value_score = 25

    engagement_score = min(100, int(reply_count * 20 + meeting_count * 25 + deal_probability * 30))
    stage_score = {
        "proposal": 90,
        "qualified": 75,
        "waiting": 65,
        "contacted": 45,
        "new": 30,
        "stale": 50,
    }.get(normalized_status, 40)
    contactability_score = 100 if has_contact_route else 0

    weights = policy.get("weights", {})
    weighted = (
        staleness_score * float(weights.get("staleness_score", 0))
        + value_score * float(weights.get("value_score", 0))
        + engagement_score * float(weights.get("engagement_score", 0))
        + stage_score * float(weights.get("stage_score", 0))
        + contactability_score * float(weights.get("contactability_score", 0))
    )
    recovery_score = max(0, min(100, int(round(weighted))))
    band = _priority_band(recovery_score, policy)
    urgency = _urgency_from_band(band)
    action_rules = policy.get("action_rules", {})
    recommended_action = action_rules.get(band, "Review manually.")
    message_angle = _message_angle(normalized_status, contactability_score)

    reasons = []
    if days_since_contact >= 30:
        reasons.append("follow-up overdue")
    if estimated_value >= 1500:
        reasons.append("meaningful deal value")
    if reply_count > 0 or meeting_count > 0:
        reasons.append("prior engagement exists")
    if normalized_status in {"proposal", "qualified"}:
        reasons.append(f"advanced stage: {normalized_status}")
    if not reasons:
        reasons.append("basic recovery candidate")

    follow_up_delta = 1 if band == "P1" else 3 if band == "P2" else 7 if band == "P3" else 14

    return LeadScore(
        lead_id=str(record.get("lead_id") or "UNKNOWN"),
        normalized_status=normalized_status,
        recovery_score=recovery_score,
        priority_band=band,
        urgency=urgency,
        recommended_action=recommended_action,
        message_angle=message_angle,
        reason_summary=", ".join(reasons),
        next_follow_up_date=(today + timedelta(days=follow_up_delta)).isoformat(),
        estimated_value=estimated_value,
    )


def build_markdown_report(result: dict[str, Any]) -> str:
    queue = result.get("top_recovery_queue", [])
    lines = [
        "# Lead Recovery Audit",
        "",
        f"Status: **{result['status']}**",
        "",
        "## Executive Summary",
        f"- Leads reviewed: {result['input_summary'].get('lead_count', 0)}",
        f"- Leads scored: {result['input_summary'].get('scored_count', 0)}",
        f"- High priority leads: {result['summary'].get('high_priority_count', 0)}",
        f"- Estimated recoverable value: {result['summary'].get('estimated_recoverable_value', 0)}",
        "",
        "## Top Recovery Opportunities",
    ]
    for item in queue[:10]:
        lines.extend(
            [
                f"### {item['lead_id']} | {item['priority_band']} | score {item['recovery_score']}",
                f"- Status: {item['normalized_status']}",
                f"- Action: {item['recommended_action']}",
                f"- Reason: {item['reason_summary']}",
                f"- Next follow-up: {item['next_follow_up_date']}",
                "",
            ]
        )
    return "\n".join(lines)


def run_lead_recovery_audit(
    input_path: str,
    mode: str = "report",
    policy_path: str = "config/lead_recovery_scoring.v1.json",
) -> dict[str, Any]:
    policy = load_policy(policy_path)
    leads = load_leads(input_path)
    today = date.today()

    scored: list[LeadScore] = []
    excluded_count = 0
    for record in leads:
        scored_lead = _score_lead(record, policy, today)
        if scored_lead is None:
            excluded_count += 1
            continue
        scored.append(scored_lead)

    scored.sort(key=lambda item: item.recovery_score, reverse=True)
    high_priority = [item for item in scored if item.priority_band == "P1"]
    estimated_recoverable_value = int(sum(item.estimated_value for item in scored[:10]))

    result = result_envelope(
        engine=ENGINE_NAME,
        mode=mode,
        status="DRY_READY" if mode == "dry" else "OK",
        input_summary={
            "lead_count": len(leads),
            "excluded_count": excluded_count,
            "scored_count": len(scored),
        },
        summary={
            "high_priority_count": len(high_priority),
            "estimated_recoverable_value": estimated_recoverable_value,
            "top_actions": [item.recommended_action for item in scored[:3]],
        },
        artifacts=[input_path, policy_path],
        recommended_next_action="Run in report mode and export the markdown summary to share with a prospect.",
    )
    result["top_recovery_queue"] = [item.__dict__ for item in scored[:10]]
    result["markdown_report"] = build_markdown_report(result)
    return result
