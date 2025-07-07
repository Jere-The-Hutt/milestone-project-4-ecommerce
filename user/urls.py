from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile_view, name='account_profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]
