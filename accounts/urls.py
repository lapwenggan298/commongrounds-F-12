from django.urls import path

from .views import ProfileUpdateView, ProfileDashboardView, ProfileCreateView, UserRegisterView

urlpatterns = [
    path('register/',UserRegisterView.as_view(), name='user_registration' ),
    path('dashboard/', ProfileDashboardView.as_view(), name='profile_dashboard'),
    path('create/', ProfileCreateView.as_view(), name='profile_create'),
    path('<str:username>/', ProfileUpdateView.as_view(), name='profile_update'),
]

app_name = "accounts"