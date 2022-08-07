from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", views.HomePage.as_view(), name="home"),
    path("results", views.video_page, name="get_results"),
    path("history", views.history, name="history"),
    path("view/<int:doc_id>", views.document, name="document"),
    path("login", LoginView.as_view(redirect_authenticated_user=True), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path(
        "signup",
        views.SignUpView.as_view(),
        name="signup",
    ),
]
