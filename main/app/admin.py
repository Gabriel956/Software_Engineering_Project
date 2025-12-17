from django.contrib import admin
from .models import Profile, Interest, Event, RSVP, Comment
# Admin configuration for Profile, Interest, Event, RSVP, and Comment models
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name')
    search_fields = ('user__username', 'display_name')
# Admin for Interest model
@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    search_fields = ('name',)
# Admin for Event model
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'starts_at', 'host', 'visibility', 'created_at')
    list_filter = ('starts_at', 'visibility', 'interests')
    search_fields = ('title', 'location', 'description')
# Admin for RSVP model
@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'event__title')
# Admin for Comment model
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'event', 'created_at')
    list_filter = ('event', 'author')
    search_fields = (
        'author__display_name',
        'author__user__username',
        'event__title',
        'text',
    )