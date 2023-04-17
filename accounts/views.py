from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, RegisterForm
from accounts.models import MyUser
from django.contrib.auth import login, logout
from app.models import Instagram

def login_view(request):
    context = {}
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST or None)
        if form.is_valid():
            user = MyUser.objects.get(email=form.cleaned_data.get("email"))
            login(request, user)
            return redirect("app:profile", slug=user.slug)
        else:
            print(form.errors)
            form = LoginForm()

    context['form'] = form
    return render(request, "login.html", context)


def register_view(request):
    context = {}
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():

            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()

            # create the Instagram object
            instagram_username = form.cleaned_data['instagram_username']
            instagram_password = form.cleaned_data['instagram_password']
            if instagram_username and instagram_password:
                instagram = Instagram.objects.create(
                    user=new_user,
                    username=instagram_username,
                    password=instagram_password,
                )
                instagram.save()

            # redirect the user to the login page
            return redirect('accounts:login')
    else:
        form = RegisterForm()
    context['form'] = form
    return render(request, "register.html", context)


def logout_view(request):
    logout(request)
    return redirect("accounts:login")