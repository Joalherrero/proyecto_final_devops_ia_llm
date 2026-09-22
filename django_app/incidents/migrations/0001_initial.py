from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Incident",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("service", models.CharField(default="django-demo", max_length=80)),
                ("log", models.TextField(max_length=5000)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Diagnosis",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("mode", models.CharField(max_length=20)),
                ("category", models.CharField(max_length=80)),
                ("severity", models.CharField(max_length=20)),
                ("summary", models.TextField()),
                ("root_cause", models.TextField()),
                ("suggested_fix", models.TextField()),
                ("evidence", models.JSONField(default=list)),
                ("model_backend", models.CharField(max_length=80)),
                ("incident", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="diagnoses", to="incidents.incident")),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
