from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


Severity = Literal["low", "medium", "high", "critical"]


CATEGORIES = [
    "python_import_error",
    "missing_env_var",
    "docker_build_failure",
    "cloud_run_startup_failure",
    "github_actions_secret_missing",
    "dependency_conflict",
    "api_timeout",
    "authentication_failure",
    "rate_limit_error",
    "database_connection_error",
    "json_output_error",
]


class TriageResult(BaseModel):
    summary: str = Field(min_length=1)
    root_cause: str = Field(min_length=1)
    severity: Severity
    suggested_fix: str = Field(min_length=1)
    category: str = Field(pattern="^(" + "|".join(CATEGORIES) + ")$")


class TriageRequest(BaseModel):
    log: str = Field(min_length=1)
    source: str | None = None
    environment: str | None = None


class TriageResponse(TriageResult):
    confidence: float | None = None
    model_backend: str
    trace_id: str | None = None
