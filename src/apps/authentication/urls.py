from django.urls import path, include
from django.contrib.auth import views as auth_views


login_view = auth_views.LoginView.as_view(template_name="ui/pages/login.html")
logout_view = auth_views.LogoutView.as_view(next_page="/")

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("oauth/", include("social_django.urls", namespace="social")),
]
