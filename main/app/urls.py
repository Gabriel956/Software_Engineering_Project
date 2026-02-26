from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Home page showing events for logged-in users
    path('', views.login_events, name='login_events'),
    # User authentication URLs
    path('signup/', views.signup, name='signup'),
    # Login
    path('events/', views.event_list, name='event_list'),
    # Create, view, and edit events
    path('events/create/', views.event_create, name='event_create'),
    # View and edit specific event
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    # Edit specific event
    path('events/<int:event_id>/edit/', views.event_edit, name='event_edit'),
    # User profile URLs
    path('profile/', views.profile_view, name='profile'),
    # Edit user profile
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    # RSVP to events
    path('events/<int:event_id>/rsvp/', views.rsvp_event, name='rsvp_event'),
    # Logout
    path('logout/', views.logout_view, name='logout'),
    # Comments on events
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    # Edit comment
    path('comments/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
]
# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)