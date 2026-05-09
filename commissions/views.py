from django.views.generic import ListView, DetailView, View, UpdateView, CreateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Case, When, Value, IntegerField, Sum

from .models import Commission, Job, JobApplication
from .forms import CommissionCreateForm

class CommissionListView(ListView):
    model = Commission
    template_name = "commissions/commission_list.html"
    context_object_name = "all_commissions"

    def get_queryset(self):
        return Commission.objects.annotate(
            custom_order=Case(
                When(status="OPEN", then=0),
                When(status="FULL", then=1),
                When(status="COMPLETED", then=2),
                When(status="DISCONTINUED", then=3),
                output_field=IntegerField(),
            )
        ).order_by("status", "-created_on")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            
            my_commissions = Commission.objects.filter(maker=profile).order_by("-created_on")
            applied_commissions = Commission.objects.filter(jobs__applications__applicant=profile).distinct()

            context['my_commissions'] = my_commissions
            context['applied_commissions'] = applied_commissions

            exclude_ids = list(my_commissions.values_list('id', flat=True)) + list(applied_commissions.values_list('id', flat=True))

            context['all_commissions'] = context['all_commissions'].exclude(id__in=exclude_ids)

            context['is_maker'] = profile.roles.filter(name="COMMISSION_MAKER").exists()

        return context

class CommissionDetailView(DetailView):
    model = Commission
    template_name = "commissions/commission_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        commission = self.get_object()
        
        total_required = commission.jobs.aggregate(total=Sum('manpower_required'))['total'] or 0
        
        accepted_count = JobApplication.objects.filter(
            job__commission=commission, 
            status="ACCEPTED"
        ).count()
        
        open_manpower = total_required - accepted_count
        
        context['total_manpower'] = total_required
        context['open_manpower'] = open_manpower
        return context
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        job_id = request.POST.get('job_id')
        job = get_object_or_404(Job, id=job_id)

        if job.status != "FULL":
            JobApplication.objects.create(job=job, applicant=request.user.profile)

        return redirect('commissions:commission_detail', pk=self.get_object().pk)

class CommissionCreateView(LoginRequiredMixin, CreateView):
    model = Commission
    form_class = CommissionCreateForm

    template_name = "commissions/commission_form.html"
    required_role = "COMMISSION_MAKER"
    
    success_url = reverse_lazy("commissions:commission_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.profile.roles.filter(name=self.required_role).exists():
            return redirect("commissions:commission_list")
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.maker = self.request.user.profile

        commission = form.save()

        Job.objects.create(
            commission=commission,
            role=form.cleaned_data['role'],
            manpower_required=form.cleaned_data['manpower_required'],
        )

        return super().form_valid(form)
    

class CommissionUpdateView(LoginRequiredMixin, UpdateView):
    model = Commission
    fields = ["title", "description", "type", "people_required", "status"]
    template_name = "commissions/commission_form.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.profile.roles.filter(name="COMMISSION_MAKER").exists():
            return redirect("commissions:commission_list")
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        response = super().form_valid(form)

        all_jobs = self.object.jobs.all()
        if all_jobs.exists() and all(job.status == "FULL" for job in all_jobs):
            self.object.status = "FULL"
            self.object.save()

        return response

    def get_success_url(self):
        return reverse_lazy("commissions:commission_detail", kwargs={"pk": self.object.pk}
        )
    
