
from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import (
    UserRegistrationView,
    UserLoginView,
    UserListView,
    UserDetailView,
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
    path('users', UserListView.as_view(), name='userlist'),
    path('users/<int:pk>', UserDetailView.as_view(),name='userdetail'),
    path('customer/loan', CustomerLoanView.as_view(),name='loanlistforcustomers' ),
    path('agent/loan', AgentLoanView.as_view() ,name='loanlistforagents'),
    path('agent/loan-detail/<int:pk>', AgentLoanDetailView.as_view(),name='loandetailforagent' ),
    path('admin/loan', AdminLoanView.as_view() ,name='loanlistforadmin' ),
    path('admin/loan-detail/<int:pk>', AdminLoanDetailView.as_view(),name='loandetailforadmin'  ),
    path('admin-agent/loan-filter/<str:filtr>/<str:value>', AdminAgentFilterView.as_view() ,name='loanfilterforadminandagent' ),
    path('customer/loan-filter/<str:filtr>/<str:value>', CustomerFilterView.as_view(),name='loanfilterforcustomer' ),
    path('logout', UserLogoutView.as_view(), name='logout'),


]