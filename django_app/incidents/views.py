"""Minimal incident lifecycle for the local course laboratory."""

import logging
import os
import re

import httpx
from django.contrib import messages
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Diagnosis, Incident


logger = logging.getLogger("incidents")
TRIAGE_URL = os.getenv("TRIAGE_URL", "http://triage:8001/triage")


def redact(text: str) -> str:
    """Basic teaching example; real log redaction requires a broader policy."""
    text = re.sub(r"(?i)(api[_-]?key|token|password|secret)\s*[=:]\s*\S+", r"\1=[REDACTED]", text)
    return text[:5000]


def index(request):
    incidents = Incident.objects.prefetch_related("diagnoses")[:30]
    return render(request, "incidents/index.html", {"incidents": incidents})


def health(request):
    return JsonResponse({"status": "ok"})


def create_demo(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    try:
        __import__("modulo_inexistente_del_laboratorio")
    except ModuleNotFoundError as exc:
        log = redact(f"ModuleNotFoundError: {exc}")
        logger.error("Incidente de demostración: %s", log)
        Incident.objects.create(service="django-demo", log=log)
    return redirect("index")


def create_custom(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    log = redact(request.POST.get("log", "").strip())
    if not log:
        messages.error(request, "Escribe un log antes de guardar el incidente.")
        return redirect("index")
    Incident.objects.create(service="django-demo", log=log)
    logger.info("Incidente manual registrado; longitud del log: %s", len(log))
    return redirect("index")


def diagnose(request, pk: int):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    incident = get_object_or_404(Incident, pk=pk)
    mode = request.POST.get("mode", "rules")
    if mode not in {"rules", "ollama"}:
        messages.error(request, "Modo de diagnóstico no admitido.")
        return redirect("index")
    try:
        response = httpx.post(
            TRIAGE_URL,
            json={"incident_id": incident.pk, "service": incident.service, "log": redact(incident.log), "mode": mode},
            timeout=100,
        )
        response.raise_for_status()
        result = response.json()
        Diagnosis.objects.create(
            incident=incident,
            mode=mode,
            category=result["category"],
            severity=result["severity"],
            summary=result["summary"],
            root_cause=result["root_cause"],
            suggested_fix=result["suggested_fix"],
            evidence=result["evidence"],
            model_backend=result["model_backend"],
        )
        messages.success(request, "Diagnóstico guardado.")
    except (httpx.HTTPError, ValueError, KeyError) as exc:
        logger.warning("El diagnóstico falló: %s", type(exc).__name__)
        messages.error(request, f"No se pudo diagnosticar el incidente ({type(exc).__name__}).")
    return redirect("index")
