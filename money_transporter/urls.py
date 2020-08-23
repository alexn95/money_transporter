from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView, TokenObtainPairView

from money_transporter import views

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),

    path('money_transporter/', views.CreateUserView.as_view(), name='money_transporter-create'),
    path('currency/', views.CurrencyListView.as_view(), name='currency-list'),
    path('transactions/', views.TransactionListView.as_view(), name='transaction-list'),
    path('transfer/', views.MakeTransferView.as_view(), name='transfer-make'),

]
