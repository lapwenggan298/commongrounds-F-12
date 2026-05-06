from django.urls import path

from .views import ProfileUpdateView, ProfileDashboardView

urlpatterns = [
    path('dashboard/', ProfileDashboardView.as_view(), name='profile_dashboard'),
    path('<str:username>/', ProfileUpdateView.as_view(), name='profile_update'),
]

app_name = "accounts"