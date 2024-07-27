from django.urls import path

from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from rest_framework_simplejwt.views import TokenVerifyView

from . import api

urlpatterns = [
    path('register/', RegisterView.as_view(), name='rest_register'),
    path('login/', LoginView.as_view(), name='rest_login'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
    path('myreservations/', api.reservations_list, name='api_reservations_list'),
    path('<uuid:pk>/', api.landlord_detail, name='api_landlrod_detail'),
    path('edit-profile',api.edit_profile,name='edit-profile'),
    path('forgot-password/',api.forgot_password,name='forgot-password'),
    path('check-otp/',api.check_otp,name='check-otp'),
    path('reset-password/',api.reset_password,name='reset-password'),
    path('get-reservations/',api.get_reservations,name='get_reservations')
]