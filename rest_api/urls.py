from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt import views as jwt_views
from .views import ActiveUserViewSet, VerificationRequestsViewSet

me_router = SimpleRouter()
me_router.register(r'user', ActiveUserViewSet, basename='active-user')

default_router = SimpleRouter()
default_router.register(
    r'verifications', VerificationRequestsViewSet, basename="verifications")

urlpatterns = [
    path('auth/token/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('auth/token/refresh/',
         jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', include(me_router.urls)),
    path('', include(default_router.urls))
]
