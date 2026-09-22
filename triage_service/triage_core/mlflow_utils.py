from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Iterator


@contextmanager
def optional_mlflow_run(experiment_name: str, run_name: str) -> Iterator[object | None]:
    """Start an MLflow run only when a tracking URI is configured."""
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
    if not tracking_uri:
        yield None
        return

    import mlflow

    os.environ.setdefault("MLFLOW_SUPPRESS_PRINTING_URL_TO_STDOUT", "true")
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)
    with mlflow.start_run(run_name=run_name) as run:
        yield run
