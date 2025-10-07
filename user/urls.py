from django.urls import path
from . import views


urlpatterns = [
    path('profile/', views.profile_view, name='account_profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('delete-account/', views.delete_account, name='delete_account'),
]
