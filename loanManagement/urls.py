
from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import (
    UserRegistrationView,
    UserLoginView,
    UserListView,
    UserDetailView,
    LoanListView,
    LoanDetailView,
    LoanFilterView,
    UserLogoutView
   
)

urlpatterns = [
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='userlist'),
    path('users/<int:pk>/', UserDetailView.as_view(),name='userdetail'),
    path('loans/', LoanListView.as_view(),name='loanlist' ),
    path('loans/<int:pk>/', LoanDetailView.as_view(),name='loandetail' ),
    path('loan-filter/<str:filtr>/<str:value>/', LoanFilterView.as_view() ,name='loanfilter' ),
    path('logout/',UserLogoutView.as_view() ,name='logout')
]