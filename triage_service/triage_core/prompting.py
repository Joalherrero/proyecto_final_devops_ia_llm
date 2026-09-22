from __future__ import annotations


SYSTEM_PROMPT = "You are a DevOps incident triage assistant. Return valid JSON only."


def build_user_prompt(log: str) -> str:
    return (
        "Analyze this DevOps incident log and return JSON with summary, root_cause, "
        "severity, suggested_fix, and category.\n\n"
        f"Log:\n{log}"
    )
