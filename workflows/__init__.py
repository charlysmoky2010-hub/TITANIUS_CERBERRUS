from core.registry import WorkflowRegistry
from workflows.lead_recovery import run_lead_recovery_audit

registry = WorkflowRegistry()
registry.register("lead_recovery_audit", run_lead_recovery_audit)

__all__ = ["registry", "run_lead_recovery_audit"]
