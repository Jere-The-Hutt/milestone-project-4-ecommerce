from django.urls import path
from . import views


app_name = 'orders'

urlpatterns = [
    path('create/<int:product_id>/', views.order_create, name='order_create'),
    path('history/<int:order_id>/', views.order_history, name='order_history'),
]
