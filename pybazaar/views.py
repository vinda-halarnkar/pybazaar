from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    return render(request, "index.html")


def home(request):
    return render(request, "home.html")


def contact(request):
    return render(request, "contact.html")
