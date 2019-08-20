from django.urls import path

from apps.staff import views


app_name = "staff"
urlpatterns = [
    path("", views.index, name="index"),
    path("histograms/", views.histograms, name="histograms"),
    path("metrics/", views.metrics, name="metrics"),
]
