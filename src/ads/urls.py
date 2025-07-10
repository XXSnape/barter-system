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
