from django.views.generic import ListView, DetailView, View, UpdateView, CreateView
from .models import Commission, Job
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class CommissionListView(ListView):
    model = Commission
    template_name = "commissions/commission_list.html"
    context_object_name = "commissions"

    def get_queryset(self):
        return Commission.objects.annotate(
            status_order=Case(
                When(status="OPEN", then=0),
                When(status="FULL", then=1),
                When(status="COMPLETED", then=2),
                When(status="DISCONTINUED", then=3),
                output_field=IntegerField(),
            )
        ).order_by("status_order", "-created_on")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        if user.is_authenticated and hasattr(user, "profile"):
            profile = user.profile

            my_commissions = Commission.objects.filter(maker=profile)

            applied_commissions = Commission.objects.filter(
                jobs__applications__applicant=profile
            ).distinct()

            exclude_ids = list(my_commissions.values_list("id", flat=True)) + \
                          list(applied_commissions.values_list("id", flat=True))

            context["my_commissions"] = my_commissions
            context["applied_commissions"] = applied_commissions
            context["commissions"] = context["commissions"].exclude(id__in=exclude_ids)

        return context

class CommissionDetailView(DetailView):
    model = Commission
    template_name = "commissions/commission_detail.html"
    context_object_name = "commission"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        commission = self.object
        return context

class CommissionCreateView(LoginRequiredMixin, CreateView):
    model = Commission
    fields = ["title", "description", "type", "people_required", "status"]
    template_name = "commissions/commission_form.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.profile.role == "Commission Maker":
            return redirect("commissions:commission_list")
        return super().dispatch(request, *args, **kwargs)
    
class CommissionUpdateView(LoginRequiredMixin, UpdateView):
    model = Commission
    fields = ["title", "description", "type", "people_required", "status"]
    template_name = "commissions/commission_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)

        return response

    def get_success_url(self):
        return reverse_lazy(
            "commissions:commission_detail",
            kwargs={"pk": self.object.pk}
        )
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.profile.role == "Commission Maker":
            return redirect("commissions:commission_list")
        return super().dispatch(request, *args, **kwargs)
