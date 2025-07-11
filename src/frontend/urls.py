from django.urls import path
from django.views.generic import TemplateView


app_name = "frontend"

urlpatterns = [
    path(
        "create/", TemplateView.as_view(template_name="frontend/create.html")
    ),
    path("", TemplateView.as_view(template_name="frontend/ads.html")),
]
