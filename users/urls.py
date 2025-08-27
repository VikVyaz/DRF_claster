from django.urls import path
from .apps import UsersConfig
from .views import PaymentListAPIView, UserCreateAPIView, UserListAPIView, UserUpdateAPIView, UserDestroyAPIView, UserRetrieveAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.permissions import AllowAny


app_name = UsersConfig.name

urlpatterns = [
    path('payment/', PaymentListAPIView.as_view(), name='payment_list'),

    path('register/', UserCreateAPIView.as_view(), name='user_register'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),

    path('list/', UserListAPIView.as_view(), name='user_list'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='user_detail'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='user_update'),
    path('delete/<int:pk>/', UserDestroyAPIView.as_view(), name='user_delete'),
]
