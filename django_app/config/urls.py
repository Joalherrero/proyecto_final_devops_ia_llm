from django.urls import path

from incidents import views


urlpatterns = [
    path("", views.index, name="index"),
    path("health/", views.health, name="health"),
    path("incidents/demo/", views.create_demo, name="create_demo"),
    path("incidents/new/", views.create_custom, name="create_custom"),
    path("incidents/<int:pk>/diagnose/", views.diagnose, name="diagnose"),
]
