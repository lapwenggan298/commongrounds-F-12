from django.urls import path

from .views import ProfileUpdateView, ProfileDashboardView

urlpatterns = [
    path('<str:username>/', ProfileUpdateView.as_view(), name='profile_update'),
    path('dashboard/', ProfileDashboardView.as_view(), name='profile_dashboard'),
]

app_name = "accounts"