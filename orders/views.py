from django.shortcuts import render, get_object_or_404
from .forms import OrderCreateForm
from shop.models import Product
from .tasks import order_created


def order_create(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            order.save()
            order_created.delay(order.id)  # Trigger the asynchronous task
            return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()

    return render(request, 'orders/order/create.html', {'form': form, 'product': product})
