from django.shortcuts import render
from django.views.generic.base import TemplateView


from django.http import HttpResponse

from .models import Commissions
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

def index(request):
    return HttpResponse('Sorry bro.')

def commission_list(request):
    commissions = Commissions.objects.all()
    context = {"commissions": commissions}
    return render(request, "ledger/commission_list.html", context)


def commission_detail(request, pk):
    commissions = Commission.objects.get(pk=pk)
    context = {"recipe": recipe}
    return render(request, "ledger/commission_detail.html", context)