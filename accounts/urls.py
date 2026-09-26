from django.urls import path

from . import views


urlpatterns = [
    # User Profile
    path(
        'profile/',
        views.profile,
        name='profile',
    ),

    # Authentication
    path(
        'register/',
        views.register,
        name='register',
    ),
    path(
        'login/',
        views.login,
        name='login',
    ),
    path(
        'logout/',
        views.logout,
        name='logout',
    ),
]