from django.db import models


class Incident(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    service = models.CharField(max_length=80, default="django-demo")
    log = models.TextField(max_length=5000)

    class Meta:
        ordering = ["-created_at"]


class Diagnosis(models.Model):
    incident = models.ForeignKey(Incident, related_name="diagnoses", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    mode = models.CharField(max_length=20)
    category = models.CharField(max_length=80)
    severity = models.CharField(max_length=20)
    summary = models.TextField()
    root_cause = models.TextField()
    suggested_fix = models.TextField()
    evidence = models.JSONField(default=list)
    model_backend = models.CharField(max_length=80)

    class Meta:
        ordering = ["-created_at"]
