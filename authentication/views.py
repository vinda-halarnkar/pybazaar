from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm
import logging

logger = logging.getLogger(__name__)

def register_view(request):
    """
    Handles user registration.

    Parameters:
    request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
    HttpResponse: A redirect response to the login page if registration is successful,
                  or renders the registration page with the registration form if the request method is GET
                  or if the form submission is invalid.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # Redirect to login page
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

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
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                logger.info(f"Successful login for user: {email}")
                return redirect("index")
            else:
                messages.error(request, "Invalid email or password")
                logger.warning(f"Failed login attempt for email: {email}")
        else:
            logger.error("Invalid login form submission")
    else:
        form = LoginForm()
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
