# app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from .models import Event  
from django.forms import ModelForm
from django import forms

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

    events = Event.objects.all
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
            "events": events,
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

<<<<<<< HEAD


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'starts_at', 'capacity', 'visibility', 'interests']
        widgets = {
            'starts_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

@login_required
def event_create(request):
    profile = request.user.profile

    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.host = profile

            event.starts_at = form.cleaned_data['starts_at']
            
            event.save()
            form.save_m2m()
            return redirect("event_detail", event_id=event.id)   # <— Redirect is valid response!
    else:
        form = EventForm()

    return render(request, "app/event_form.html", {"form": form})

@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, "app/event_detail.html", {"event": event})

@login_required
def event_list(request):
    events = Event.objects.order_by('starts_at')
    return render(request, "app/event_list.html", {"events": events})

=======
def profile(request):
    
    
    return render(request, "app/profile.html")

def events(request, id):
    
    id = get_object_or_404(Event, pk=id)
    return render(request, "app/events.html", {"id": id})
>>>>>>> 2123a0acd1f7833841a5be1974fa9242bb62f671
