# app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from .models import Event  # ← add Comment, Interest later if you need

def login_events(request):
    # If user is already logged in, show events screen
    if request.user.is_authenticated:
        events = (
            Event.objects.filter(starts_at__gte=timezone.now())
            .order_by("starts_at")
        )
        # You can also prefetch rsvps/comments for efficiency later
        return render(
            request,
            "app/login_events.html",
            {
                "events": events,
                "logged_in": True,
            },
        )

    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("login_events")
        else:
            error = "Invalid username or password."

    return render(
        request,
        "app/login_events.html",
        {
            "error": error,
            "logged_in": False,
        },
    )

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login_events")
    else:
        form = UserCreationForm()

    return render(request, "app/signup.html", {"form": form})
