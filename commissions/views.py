from django.views.generic import ListView, DetailView, View, UpdateView
from .models import Commission, Job
from django.shortcuts import get_object_or_404, redirect
from .services import CommissionService
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class CommissionListView(ListView):
    model = Commission
    template_name = "commissions/commission_list.html"
    context_object_name = "commissions"

    def get_queryset(self):
        return Commission.objects.all().order_by("created_on")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        if user.is_authenticated:
            profile = user.profile

            my_commissions = Commission.objects.filter(maker=profile)

            applied_commissions = Commission.objects.filter(
                jobs__applications__applicant=profile
            ).distinct()

            all_commissions = context["commissions"].exclude(
                id__in=my_commissions.union(applied_commissions)
            )

            context["my_commissions"] = my_commissions
            context["applied_commissions"] = applied_commissions
            context["commissions"] = all_commissions

        return context

class CommissionDetailView(DetailView):
    model = Commission
    template_name = "commissions/commission_detail.html"
    context_object_name = "commission"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        commission = self.object

        context["summary"] = CommissionService.get_commission_summary(
            commission
        )

        return context

class ApplyToJobView(LoginRequiredMixin, View):

    def post(self, request, pk):
        job = get_object_or_404(Job, pk=pk)

        CommissionService.apply_to_job(
            applicant=request.user.profile,
            job=job
        )

        return redirect(
            "commissions:commission_detail",
            pk=job.commission.pk
        )
    
from django.views.generic import CreateView


class CommissionCreateView(LoginRequiredMixin, CreateView):
    model = Commission
    fields = ["title", "description", "type", "people_required", "status"]
    template_name = "commissions/commission_form.html"

    def form_valid(self, form):
        commission = CommissionService.create_commission(
            author=self.request.user.profile,
            data=form.cleaned_data,
            jobs_data=[{
                "role": request.POST.get("role"),
                "manpower_required": request.POST.get("manpower_required"),
            }]
        )

        return redirect("commissions:commission_detail", pk=commission.pk)
    
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

        CommissionService.sync_commission_status(self.object)

        return response

    def get_success_url(self):
        return reverse_lazy(
            "commissions:commission_detail",
            kwargs={"pk": self.object.pk}
        )
    
