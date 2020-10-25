
from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import (
    UserRegistrationView,
    UserLoginView,
    UserListView,
    UserDetailView,
    #LoanView,
    CustomerLoanView,
    AgentLoanView,
    AgentLoanDetailView,
    AdminLoanView,
    AdminLoanDetailView,
    AdminAgentFilterView,
    CustomerFilterView,
    UserLogoutView
)

urlpatterns = [
    path('token/obtain', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register', UserRegistrationView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('users', UserListView.as_view(), name='users'),
    path('users/<int:pk>', UserDetailView.as_view()),
    path('customer/loan', CustomerLoanView.as_view() ),
    path('agent/loan', AgentLoanView.as_view() ),
    path('agent/loan-detail/<int:pk>', AgentLoanDetailView.as_view() ),
    path('admin/loan', AdminLoanView.as_view() ),
    path('admin/loan-detail/<int:pk>', AdminLoanDetailView.as_view() ),
    path('admin-agent/loan-search/<str:filtr>/<str:value>', AdminAgentFilterView.as_view() ),
    path('customer/loan-search/<str:filtr>/<str:value>', CustomerFilterView.as_view() ),
    path('logout', UserLogoutView.as_view(), name='logout'),


]