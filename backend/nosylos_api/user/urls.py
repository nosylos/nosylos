from django.urls import include
from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework_simplejwt.views import TokenRefreshView
from user.app_data.views.jwt_views import CustomTokenObtainPairView
from user.app_data.views.password_views import PasswordViewSet
from user.app_data.views.user_views import RegistrationViewSet
from user.app_data.views.user_views import UserViewSet


router = routers.DefaultRouter()
router.register(r"^users/register", RegistrationViewSet, basename="users")
router.register(r"^users", UserViewSet, basename="users")
router.register(r"^auth/password", PasswordViewSet, basename="auth")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "api/token/",
        CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    path(
        "api/token/blacklist/",
        TokenBlacklistView.as_view(),
        name="token_blacklist",
    ),
]
