from django.urls import path
from . import views


app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path(
        '<int:id>/<slug:slug>/',
        views.product_detail,
        name='product_detail'
    ),
    path(
        'custom-request/',
        views.custom_package_request,
        name='custom_package_request'
        ),
    path(
        'custom-request/thanks/',
        views.custom_request_thanks,
        name='custom_request_thanks'
        ),
]
