from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActivityViewSet, UserEntryViewSet

router = DefaultRouter()
router.register(r'activities', ActivityViewSet)
router.register(r'entries', UserEntryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
