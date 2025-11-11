from django.contrib import admin
from .models import Profile, Interest, Event, RSVP, Comment

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name')
    search_fields = ('user__username', 'display_name')

@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'starts_at', 'host', 'visibility', 'created_at')
    list_filter = ('starts_at', 'visibility', 'interests')
    search_fields = ('title', 'location', 'description')

@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'event__title')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'created_at')
    search_fields = ('user__username', 'event__title', 'body')
