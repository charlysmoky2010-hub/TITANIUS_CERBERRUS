from __future__ import annotations

from typing import Any, Callable

WorkflowRunner = Callable[..., dict[str, Any]]


class WorkflowRegistry:
    def __init__(self) -> None:
        self._runners: dict[str, WorkflowRunner] = {}

    def register(self, name: str, runner: WorkflowRunner) -> None:
        key = name.strip().lower()
        if not key:
            raise ValueError("Workflow name cannot be empty.")
        self._runners[key] = runner

    def get(self, name: str) -> WorkflowRunner:
        key = name.strip().lower()
        if key not in self._runners:
            raise KeyError(f"Unknown workflow: {name}")
        return self._runners[key]

    def list_names(self) -> list[str]:
        return sorted(self._runners.keys())
