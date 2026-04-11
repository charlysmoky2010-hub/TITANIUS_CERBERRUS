from workflows import registry
from workflows.lead_recovery import run_lead_recovery_audit


def test_registry_contains_lead_recovery() -> None:
    assert "lead_recovery_audit" in registry.list_names()


def test_lead_recovery_report_shape() -> None:
    result = run_lead_recovery_audit("samples/leads_demo.v1.json", mode="report")
    assert result["engine"] == "LEAD_RECOVERY_AUDIT"
    assert result["status"] == "OK"
    assert result["input_summary"]["lead_count"] == 5
    assert result["input_summary"]["scored_count"] >= 1
    assert "top_recovery_queue" in result
    assert "markdown_report" in result
    assert result["top_recovery_queue"][0]["recovery_score"] >= result["top_recovery_queue"][-1]["recovery_score"]


def test_lead_recovery_dry_mode() -> None:
    result = run_lead_recovery_audit("samples/leads_demo.v1.json", mode="dry")
    assert result["status"] == "DRY_READY"
