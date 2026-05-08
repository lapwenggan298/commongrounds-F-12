from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Profile


def create_profile(user):
    Profile.objects.create(user=user)