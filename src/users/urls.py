from django.urls import path
from .views import CreateUserView


app_name = "users"


urlpatterns = [
    path(
        "sign-up",
        CreateUserView.as_view(),
        name="sign-up",
    ),
]
