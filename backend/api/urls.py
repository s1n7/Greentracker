from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import ActivityViewSet, UserEntryViewSet, RegisterUserView, LoginView, LogoutView

router = DefaultRouter()
router.register(r'activities', ActivityViewSet)
router.register(r'entries', UserEntryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', LoginView.as_view(), name='api_login'),
    path('auth/register/', RegisterUserView.as_view(), name='api_register'),
    path('auth/logout/', LogoutView.as_view(), name='api_logout'),
]
