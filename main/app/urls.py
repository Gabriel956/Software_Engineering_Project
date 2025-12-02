from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_events, name='login_events'),
    path('signup/', views.signup, name='signup'),
<<<<<<< HEAD

    path('events/', views.event_list, name='event_list'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
=======
    path('profile/', views.profile, name='profile'),
    path('events/<int:id>/', views.events, name='events'),
>>>>>>> 2123a0acd1f7833841a5be1974fa9242bb62f671
]
