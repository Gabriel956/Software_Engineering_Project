from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_events, name='login_events'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('events/<int:id>/', views.events, name='events'),
]
