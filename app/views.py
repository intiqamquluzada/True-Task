from django.shortcuts import render, get_object_or_404
from accounts.models import MyUser
from .tasks import scrape_data_copy


def my_profile(request, slug):
    context = {}
    user = get_object_or_404(MyUser, slug=slug)
    scrape_data_copy(slug)
    context['user'] = user
    return render(request, "profile.html", context)
