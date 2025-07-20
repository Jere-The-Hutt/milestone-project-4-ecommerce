from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render, get_object_or_404
from .forms import OrderCreateForm
from shop.models import Product
from .models import Order
from .tasks import order_created
from django.contrib.auth.decorators import login_required
import weasyprint
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.template.loader import render_to_string


@login_required
def order_create(request, product_id):
    """
    Handle order creation for a specific product.
    Saves order info and stores order ID in session.
    """
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

    return render(request, 'orders/order/create.html',
                  {'form': form,
                   'product': product})


@login_required
def order_history(request, order_id):
    """
    Show a specific past order belonging to the current user.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order/history.html', {'order': order})


@staff_member_required
def admin_order_detail(request, order_id):
    """
    Display full order details for staff members in the admin dashboard.
    """
    order = get_object_or_404(Order, id=order_id)
    return render(
        request, 'orders/order/detail.html', {'order': order}
        )


@staff_member_required
def admin_order_pdf(request, order_id):
    """
    Generate and return a PDF invoice for an order (admin only).
    """
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(
        response,
        stylesheets=[weasyprint.CSS(finders.find('css/pdf.css'))]
    )
    return response
