from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

# Create your models here.
# models needed for, events, profiles, and any other data that needs to be stored in the database
# profile model need name, email, phone number, birthday 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)

    interests = models.ManyToManyField('Interest', blank=True)

    def __str__(self):
        return self.display_name 
    
class Interest(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Event(models.Model):
    PUBLIC = 'public'
    PRIVATE = 'private'
    VISIBILITY_CHOICES = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    host = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='hosted_events')

    location = models.CharField(max_length=255)
    starts_at = models.DateTimeField()
    capacity = models.PositiveIntegerField()
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default=PUBLIC)
    interests = models.ManyToManyField(Interest, blank=True, related_name='events')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class RSVP(models.Model):
    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'event'], name='unique_rsvp')]
        
    GOING = 'going'
    MAYBE = 'maybe'
    NO = 'no'
    STATUS_CHOICES = [
        (GOING, 'Going'),
        (MAYBE, 'Maybe'),
        (NO, 'Not going')
    ]
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvps')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



# events should have name, date, time, location, description, and a list of attendees (which can be a many-to-many relationship with the profile model)



# rsvp model should have a ref to the event, a ref to the profile, and a status (attending, not attending, maybe)

    
    #maybe add comments to event model for attendees to leave comments about the event, number of attendees, and a way to track the number of people attending the event.
    #should there be a model for event planner? This could be a user who creates events and manages them. It could have a one-to-many relationship with the event model, where one planner can create many events.
# what other models do we need?