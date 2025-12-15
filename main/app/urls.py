from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_events, name='login_events'),
    path('signup/', views.signup, name='signup'),
    path('events/', views.event_list, name='event_list'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/<int:event_id>/edit/', views.event_edit, name='event_edit'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('events/<int:event_id>/rsvp/', views.rsvp_event, name='rsvp_event'),
    path('logout/', views.logout_view, name='logout'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('comments/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)