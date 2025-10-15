from django.urls import path
from . import views


app_name = 'orders'

urlpatterns = [
     path('create/<int:product_id>/',
          views.order_create,
          name='order_create'),
     path('history/<int:order_id>/',
          views.order_history,
          name='order_history'),
     path('admin/order/<int:order_id>/',
          views.admin_order_detail,
          name='admin_order_detail'),
     path('admin/order/<int:order_id>/pdf/',
          views.admin_order_pdf,
          name='admin_order_pdf'),
     path('<int:order_id>/invoice/',
          views.download_invoice,
          name='download_invoice'),
]
