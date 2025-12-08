# app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Event, RSVP, Comment, Interest, Profile
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

class SignUpForm(UserCreationForm):
    display_name = forms.CharField(max_length = 20, required=False, label = 'Display Name')
    bio = forms.CharField(widget = forms.Textarea, required=False, label = 'Bio')
    interests = forms.ModelMultipleChoiceField(queryset=Interest.objects.all(), widget=forms.CheckboxSelectMultiple, required=False, label='Interests')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'display_name', 'bio', 'interests')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            #creates the user
            user = form.save()
            #creates the profile
            profile = user.profile
            #fill in extra profile info
            profile.display_name = form.cleaned_data.get('display_name', '')
            profile.bio = form.cleaned_data.get('bio', '')
            profile.save()

            #set many-to-many interests
            interests = form.cleaned_data.get('interests')
            if interests:
                profile.interests.set(interests)

            #log the user in immediately after signup
            login(request, user)

            #redirect to events page
            return redirect('event_list')
    else:
        form = SignUpForm()

    return render(request, 'app/signup.html', {'form': form})





class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = [
            'title',
            'description',
            'location',
            'starts_at',
            'capacity',
            'visibility',
            'interests',
        ]
        widgets = {
            'starts_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'interests': forms.CheckboxSelectMultiple(), # multi-select dropdown
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Load all available interests for dropdown
        self.fields['interests'].queryset = Interest.objects.all()

@login_required
def event_create(request):
    profile = request.user.profile

    if profile.display_name:
        initial = profile.display_name[0].upper()
    else:
        username = request.user.username or ""
        initial = (username[0] if username else "U").upper()

    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.host = profile
            event.starts_at = form.cleaned_data['starts_at']
            event.save()
            form.save_m2m()
            return redirect("event_detail", event_id=event.id)
    else:
        form = EventForm()

    # 👇 add initial here (adjust attribute/method to match your Profile model)
    return render(
        request,
        "app/event_form.html",
        {
            "form": form,
            "initial": initial,
        },
    )


@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    profile = request.user.profile

    # Avatar initial
    if profile.display_name:
        initial = profile.display_name[0].upper()
    else:
        username = request.user.username or ""
        initial = (username[0] if username else "U").upper()

    my_rsvp = RSVP.objects.filter(user=profile, event=event).first()
    attendees = RSVP.objects.filter(event=event)

    # Handle new comment
    if request.method == "POST" and "comment_submit" in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.event = event
            comment.author = profile
            comment.save()
            return redirect("event_detail", event_id=event.id)
    else:
        comment_form = CommentForm()

    comments = event.comments.select_related("author", "author__user")

    return render(request, "app/event_detail.html", {
        "event": event,
        "my_rsvp": my_rsvp,
        "attendees": attendees,
        "initial": initial,
        "comment_form": comment_form,
        "comments": comments,
    })
@login_required
def event_list(request):
    profile = request.user.profile

    # Avatar initial like on profile page
    if profile.display_name:
        initial = profile.display_name[0].upper()
    else:
        username = request.user.username or "U"
        initial = username[0].upper()

    # Get all events (you can filter/sort later)
    events = Event.objects.all().order_by("starts_at")

    rsvps = RSVP.objects.filter(user=profile)
    rsvp_map = {r.event_id: r.status for r in rsvps}

    return render(request, "app/event_list.html", {
        "events": events,
        "initial": initial,
        "rsvp_map": rsvp_map,
    })


@login_required
def profile_view(request):
    profile = request.user.profile
    if profile.display_name:
        initial = profile.display_name[0].upper()
    else:
        username = request.user.username or 'U'
        initial = username[0].upper()

    attending_rsvps = (RSVP.objects.filter(user=profile, status='going').select_related('event').order_by('event__starts_at'))

    return render(request, "app/profile.html", {"profile": profile, "initial": initial, "attending_rsvps": attending_rsvps})

class ProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['display_name', 'bio', 'interests']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'interests': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['interests'].queryset = Interest.objects.all()

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment...'}),}
        labels = {'text': 'Add a comment',}

@login_required
def edit_comment(request, comment_id):
    profile = request.user.profile
    comment = get_object_or_404(Comment, id=comment_id, author=profile)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("event_detail", event_id=comment.event.id)
    else:
        form = CommentForm(instance=comment)

    # Small, focused edit page
    return render(request, "app/edit_comment.html", {
        "form": form,
        "comment": comment,
    })


@login_required
def delete_comment(request, comment_id):
    profile = request.user.profile
    comment = get_object_or_404(Comment, id=comment_id, author=profile)

    event_id = comment.event.id

    if request.method == "POST":
        comment.delete()
        return redirect("event_detail", event_id=event_id)

    # Optional: simple confirm page
    return render(request, "app/confirm_delete_comment.html", {
        "comment": comment,
    })


@login_required
def edit_profile(request):
    profile = request.user.profile
    if profile.display_name:
        initial = profile.display_name[0].upper()
    else:
        username = request.user.username or 'U'
        initial = username[0].upper()


    if request.method == "POST":
        form = ProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileEditForm(instance=profile)

    return render(request, "app/edit_profile.html", {"form": form, "initial": initial})

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

