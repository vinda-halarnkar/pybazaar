from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm
import logging

logger = logging.getLogger(__name__)


@requires_csrf_token
def register_view(request):
    """
    Handles user registration.

    Parameters:
    request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
    HttpResponse: A redirect response to the login page if registration is successful,
                  or renders the registration page with the registration form
                   if the request method is GET
                  or if the form submission is invalid.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        # TODO: CHeck which scenarios form.is_valid is used
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            messages.error(request, "There were errors in the form. Please correct them.")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


@requires_csrf_token
def login_view(request):
    """
    Handles user login.

    Parameters:
    request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
    HttpResponse: A redirect response to the index page if login is successful,
                  or renders the login page with an error message if login fails.
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                messages.error(
                    request,
                    "Invalid email or password. Please check your credentials and try again.",
                )
        else:
            messages.error(request, "There were errors in the form. Please correct them.")
    else:
        form = LoginForm()
        print(form)
    return render(request, "login.html", {"form": form})


@login_required
def logout_view(request):
    """
    Logs out the authenticated user and redirects to the login page.

    Parameters:
    request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
    HttpResponse: A redirect response to the login page.
    """
    logout(request)
    return redirect("login")
