from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_events, name='login_events'),
    path('signup/', views.signup, name='signup'),
    path('events/', views.event_list, name='event_list'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('profile/', views.profile_view, name='profile'),
    path('events/<int:event_id>/rsvp/', views.rsvp_event, name='rsvp_event'),
    path('logout/', views.logout_view, name='logout'),
]
