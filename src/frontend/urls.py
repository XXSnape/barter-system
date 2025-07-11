from django.urls import path
from django.views.generic import TemplateView


app_name = "frontend"

urlpatterns = [
    path(
        "ads/",
        TemplateView.as_view(template_name="frontend/ad-list.html"),
        name="ad-list",
    ),
    path(
        "ads/<int:id>/",
        TemplateView.as_view(template_name="frontend/ad-detail.html"),
        name="ad-detail",
    ),
    path(
        "ads/create/",
        TemplateView.as_view(template_name="frontend/ad-create.html"),
        name="ad-create",
    ),
    path(
        "ads/<int:id>/edit/",
        TemplateView.as_view(template_name="frontend/ad-edit.html"),
        name="ad-edit",
    ),
    path(
        "proposals/",
        TemplateView.as_view(template_name="frontend/proposal-list.html"),
        name="proposal-list",
    ),
    path(
        "proposals/<int:id>/",
        TemplateView.as_view(template_name="frontend/proposal-detail.html"),
        name="proposal-detail",
    ),
]
