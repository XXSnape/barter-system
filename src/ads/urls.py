from django.urls import path
from django.views.generic import TemplateView

from .views import AdViewSet, ExchangeProposalViewSet
from rest_framework.routers import DefaultRouter


app_name = "ads"


router = DefaultRouter()
router.register(r"ads", AdViewSet)
router.register(
    r"proposals",
    ExchangeProposalViewSet,
    basename="proposals",
)


urlpatterns = router.urls
