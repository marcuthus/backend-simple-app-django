from django.urls import path
from .views import (
    SignInView,
    SignUpView,
    RefreshTokenView,
    MeView,
    ChangePasswordView,
)

urlpatterns = [
    path('sign-in/', SignInView.as_view(), name='auth-sign-in'),
    path('sign-up/', SignUpView.as_view(), name='auth-sign-up'),
    path('refresh-token/', RefreshTokenView.as_view(), name='auth-refresh-token'),
    path('me/', MeView.as_view(), name='auth-me'),
    path('change-password/', ChangePasswordView.as_view(), name='auth-change-password'),
]
