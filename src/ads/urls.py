from .views import AdViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"ads", AdViewSet)


urlpatterns = router.urls
