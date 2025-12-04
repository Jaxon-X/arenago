
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views  import StartRegistrationView, VerifyRegistrationView

urlpatterns = [
    path('register/start/', StartRegistrationView.as_view(), name='start_register'),
    path('register/verify/', VerifyRegistrationView.as_view(), name='verify_register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]





