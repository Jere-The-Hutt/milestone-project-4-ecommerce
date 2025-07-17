from io import BytesIO
import logging
import weasyprint
from celery import shared_task
from django.contrib.staticfiles import finders
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from orders.models import Order

logger = logging.getLogger(__name__)


@shared_task
def payment_completed(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully paid.
    """
    try:
        order = Order.objects.get(id=order_id)
        subject = f'My Shop - Invoice no. {order.id}'
        message = 'Please, find attached the invoice for your recent purchase.'
        email = EmailMessage(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [order.email]
        )

        # generate PDF
        html = render_to_string('orders/order/pdf.html', {'order': order})
        out = BytesIO()
        stylesheets = [weasyprint.CSS(finders.find('css/pdf.css'))]
        weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

        # attach PDF file
        email.attach(
            f'order_{order.id}.pdf', out.getvalue(), 'application/pdf'
        )

        # send e-mail
        email.send()
        logger.info(
            f"Order confirmation email sent for order {order.id} to {order.email}"
            )

    except Exception as e:
        logger.error(
            f"Failed to send confirmation email for order {order_id}: {e}"
            )
