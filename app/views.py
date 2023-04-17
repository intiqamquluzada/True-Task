from django.shortcuts import render, get_object_or_404
from accounts.models import MyUser


def my_profile(request, slug):
    context = {}
    user = get_object_or_404(MyUser, slug=slug)
    context['user'] = user
    return render(request, "profile.html", context)
