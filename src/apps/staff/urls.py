from django.urls import path

from apps.staff import views


app_name = "staff"

urlpatterns = [path("", views.home, name="home")]
