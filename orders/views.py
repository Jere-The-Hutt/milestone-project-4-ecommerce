from django.shortcuts import redirect, render, get_object_or_404
from .forms import OrderCreateForm
from shop.models import Product
from .models import Order
from .tasks import order_created
from django.contrib.auth.decorators import login_required


@login_required
def order_create(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            order.user = request.user
            order.save()
            order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect('payment:process')
    else:
        form = OrderCreateForm()

    return render(request, 'orders/order/create.html', {'form': form, 'product': product})


@login_required
def order_history(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order/history.html', {'order': order})
