from django.urls import path
from .views import CommissionListView, CommissionDetailView, CommissionUpdateView, ApplyToJobView, CommissionCreateView

app_name = "commissions"

urlpatterns = [
    path(
        "requests/",
        CommissionListView.as_view(),
        name="commission_list",
    ),
    path(
        "request/<int:pk>/",
        CommissionDetailView.as_view(),
        name="commission_detail",
    ),
    path(
        "request/add/",
        CommissionCreateView.as_view(),
        name="commission_create",
    ),
    path(
        "request/<int:pk>/edit/",
        CommissionUpdateView.as_view(),
        name="commission_update",
    ),
    path(
        "job/<int:pk>/apply/",
        ApplyToJobView.as_view(),
        name="apply_to_job",
    ),
]
