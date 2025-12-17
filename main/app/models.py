from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

# Create your models here.
# models needed for, events, profiles, and any other data that needs to be stored in the database
# profile model need name, email, phone number, birthday 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    fullname = models.CharField(max_length=100, blank=True)
    birthday = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)


    display_name = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)

    interests = models.ManyToManyField('Interest', blank=True)

    def __str__(self):
        return self.display_name

# Interest model for user interests
class Interest(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
# Event model to store event details
class Event(models.Model):
    # Event visibility choices
    PUBLIC = 'public'
    PRIVATE = 'private'
    VISIBILITY_CHOICES = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
    ]
    # Optional image for the event
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    # Event owner (creator)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='events_created')
    # Event details
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    # Event host (Profile)
    host = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='hosted_events')
    # Event location and time
    location = models.CharField(max_length=255)
    starts_at = models.DateTimeField()
    # Optional end time
    ends_at = models.DateTimeField(blank=True, null=True)
    capacity = models.PositiveIntegerField()
    # Event visibility
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default=PUBLIC)
    interests = models.ManyToManyField(Interest, blank=True, related_name='events')
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['starts_at']
        indexes = [
            models.Index(fields=['starts_at']),
        ]

    def __str__(self):
        return self.title
# RSVP model to track user responses to events    
class RSVP(models.Model):
    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'event'], name='unique_rsvp')]
    # RSVP status choices
    GOING = 'going'
    MAYBE = 'maybe'
    NO = 'no'
    STATUS_CHOICES = [
        (GOING, 'Going'),
        (MAYBE, 'Maybe'),
        (NO, 'Not going')
    ]
    # RSVP details
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvps')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

# Comment model for event comments
class Comment(models.Model):
    # Comment details
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.user.display_name} on {self.event.title}'



# events should have name, date, time, location, description, and a list of attendees (which can be a many-to-many relationship with the profile model)



# rsvp model should have a ref to the event, a ref to the profile, and a status (attending, not attending, maybe)

    
    #maybe add comments to event model for attendees to leave comments about the event, number of attendees, and a way to track the number of people attending the event.
    #should there be a model for event planner? This could be a user who creates events and manages them. It could have a one-to-many relationship with the event model, where one planner can create many events.
# what other models do we need?