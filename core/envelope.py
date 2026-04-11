from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def result_envelope(
    *,
    engine: str,
    mode: str,
    status: str,
    input_summary: dict[str, Any] | None = None,
    summary: dict[str, Any] | None = None,
    artifacts: list[str] | None = None,
    recommended_next_action: str = "",
) -> dict[str, Any]:
    return {
        "engine": engine,
        "mode": mode,
        "status": status,
        "timestamp_utc": now_utc_iso(),
        "input_summary": input_summary or {},
        "summary": summary or {},
        "artifacts": artifacts or [],
        "recommended_next_action": recommended_next_action,
    }
