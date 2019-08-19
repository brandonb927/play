from django.urls import path

from apps.staff import views


app_name = "staff"

urlpatterns = [
    path("", views.index, name="index"),
    path("reports/user/", views.user_report, name="user-report"),
]
