from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.conf import settings
from .forms import RegistrationForm, AccountAuthenticationForm
from .models import Profile

User = settings.AUTH_USER_MODEL


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    return redirect


def profile(request, username):
    profile = Profile.objects.get(user__username=username)
    return render(request, "profile.html", {"profile": profile})


def register(request):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"You are already logged in{user.username}")
    context = {}
    if request.method == "POST":
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email").lower()
            raw_password = form.cleaned_data.get("password1")
            account = authenticate(email=email, password=raw_password)
            auth_login(request, account)
            destination = get_redirect_if_exists(request)
            if destination:
                return redirect(destination)
        return redirect("login")
    else:
        context["registration_form"] = form
    return render(request, "register.html", context)


def login(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        form = AccountAuthenticationForm(request.POST or None)
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("dashboard")
    else:
        form = AccountAuthenticationForm()
    context["login_form"] = form
    return render(request, "login.html", context)


def logout(request):
    auth_logout(request)
    return redirect("/")
