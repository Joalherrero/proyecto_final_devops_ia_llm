from __future__ import annotations

from triage_core.schema import TriageResult


def triage_with_rules(log: str) -> TriageResult:
    """Deterministic baseline used for tests, demos, and API fallback."""
    text = log.lower()

    if "modulenotfounderror" in text or "no module named" in text or "importerror" in text:
        return TriageResult(
            summary="The Python runtime cannot import a required module.",
            root_cause="The package path, dependency installation, or module structure is incorrect.",
            severity="medium",
            suggested_fix="Verify PYTHONPATH, package layout, __init__.py files, and dependency installation in CI.",
            category="python_import_error",
        )

    if "environment variable" in text or "env var" in text or "secret" in text and "not found" in text:
        return TriageResult(
            summary="The application or workflow is missing required configuration.",
            root_cause="A required environment variable or secret is not available at runtime.",
            severity="high",
            suggested_fix="Add the missing value to GitHub Actions secrets, Cloud Run environment variables, or Secret Manager.",
            category="missing_env_var",
        )

    if "docker" in text and ("failed" in text or "returned a non-zero code" in text or "no such file" in text):
        return TriageResult(
            summary="The Docker image build failed.",
            root_cause="The Dockerfile references a missing file, invalid build step, or unavailable dependency.",
            severity="medium",
            suggested_fix="Reproduce the Docker build locally, check COPY paths, and verify dependency installation steps.",
            category="docker_build_failure",
        )

    if "cloud run" in text and ("port" in text or "listen" in text or "revision failed" in text):
        return TriageResult(
            summary="The Cloud Run revision failed to become healthy.",
            root_cause="The container is not listening on the expected PORT or exits during startup.",
            severity="high",
            suggested_fix="Ensure the app binds to the PORT environment variable and inspect startup logs for crashes.",
            category="cloud_run_startup_failure",
        )

    if "github actions" in text and ("secret" in text or "secrets" in text):
        return TriageResult(
            summary="The GitHub Actions workflow cannot access a required secret.",
            root_cause="The secret is missing, misnamed, or unavailable for the event type.",
            severity="high",
            suggested_fix="Check repository secrets, environment protection rules, and whether the workflow runs from a fork.",
            category="github_actions_secret_missing",
        )

    if "version conflict" in text or "resolutionimpossible" in text or "dependency conflict" in text:
        return TriageResult(
            summary="Dependency resolution failed because package constraints conflict.",
            root_cause="Two or more dependencies require incompatible package versions.",
            severity="medium",
            suggested_fix="Relax version pins, update the lock file, or align transitive dependency versions.",
            category="dependency_conflict",
        )

    if "timeout" in text or "timed out" in text or "deadline exceeded" in text:
        return TriageResult(
            summary="A request or job exceeded its allowed execution time.",
            root_cause="The service is slow, unavailable, or the timeout is too strict for the operation.",
            severity="medium",
            suggested_fix="Check downstream latency, add retries/backoff, and tune timeout settings with monitoring data.",
            category="api_timeout",
        )

    if "unauthorized" in text or "permission denied" in text or "403" in text or "401" in text:
        return TriageResult(
            summary="The request failed because authentication or authorization was rejected.",
            root_cause="Credentials are missing, expired, or do not have the required IAM/API permissions.",
            severity="high",
            suggested_fix="Verify service account bindings, API tokens, scopes, and secret injection into the runtime.",
            category="authentication_failure",
        )

    if "rate limit" in text or "429" in text or "quota exceeded" in text:
        return TriageResult(
            summary="The service is being throttled by a quota or rate limit.",
            root_cause="The caller exceeded provider limits or lacks sufficient quota for the current load.",
            severity="medium",
            suggested_fix="Add exponential backoff, reduce concurrency, cache repeated calls, or request more quota.",
            category="rate_limit_error",
        )

    if "database" in text or "postgres" in text or "connection refused" in text or "sqlalchemy" in text:
        return TriageResult(
            summary="The application cannot connect to the database.",
            root_cause="Database credentials, network access, instance health, or connection configuration is wrong.",
            severity="critical",
            suggested_fix="Check database health, connection string, credentials, Cloud SQL connector settings, and IAM roles.",
            category="database_connection_error",
        )

    if "json" in text or "schema" in text or "validationerror" in text:
        return TriageResult(
            summary="The LLM or service returned output that does not match the expected schema.",
            root_cause="The prompt, parser, or response validation contract is not strict enough.",
            severity="low",
            suggested_fix="Tighten the prompt, add JSON schema validation, and retry with structured output constraints.",
            category="json_output_error",
        )

    return TriageResult(
        summary="The incident needs manual investigation.",
        root_cause="The log does not match a known triage pattern.",
        severity="medium",
        suggested_fix="Inspect the full logs, recent deploys, environment changes, and service health metrics.",
        category="api_timeout",
    )
