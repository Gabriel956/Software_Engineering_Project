# app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from .models import Event, Profile, Interest, RSVP, Comment
from django.forms import ModelForm
from django import forms

def login_events(request):
    # If already logged in, go straight to events
    if request.user.is_authenticated:
        return redirect("event_list")

    error = None

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("event_list")   # show events AFTER login
        else:
            error = "Invalid username or password."

    # Just show login form (no events here)
    return render(request, "app/login_events.html", {"error": error})


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

    #gets users rsvp status for the event
    my_rsvp = RSVP.objects.filter(user=request.user.profile, event=event).first()

    #attendees list
    attendees = event.rsvps.select_related('user')

    return render(request,"app/event_detail.html",{"event": event,"my_rsvp": my_rsvp,"attendees": attendees,},)

@login_required
def event_list(request):
    events = Event.objects.order_by('starts_at')
    return render(request, "app/event_list.html", {"events": events})

@login_required
def profile_view(request):
    profile = request.user.profile
    return render(request, "app/profile.html", {"profile": profile})

@login_required
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    profile = request.user.profile

    if request.method == "POST":
        status = request.POST.get("status")

        if status in dict(RSVP.STATUS_CHOICES):
            RSVP.objects.update_or_create(
                user=profile,
                event=event,
                defaults={"status": status},
            )
    return redirect("event_detail", event_id=event.id)

def logout_view(request):
    logout(request)
    return redirect("login_events")

