from django.urls import path
import rest_framework_simplejwt.views as jwt_views
from .views import AccountView

urlpatterns = [
    path("accounts/", AccountView.as_view()),
    path("login/", jwt_views.TokenObtainPairView.as_view()),
]