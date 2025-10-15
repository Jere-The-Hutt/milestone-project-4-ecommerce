from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order
from .utils import generate_order_pdf
import logging

logger = logging.getLogger(__name__)


@shared_task
def payment_completed(order_id):
    """
    Task to send an e-mail notification when an order is successfully paid.
    """
    try:
        order = Order.objects.get(id=order_id)
        subject = f'WebDev4U - Invoice no. {order.id}'
        message = 'Please, find attached the invoice for your recent purchase.'
        email = EmailMessage(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [order.email]
        )
        # generate PDF
        pdf = generate_order_pdf(order)
        # attach PDF file
        email.attach(
            f'order_{order.id}.pdf',
            pdf.getvalue(),
            'application/pdf'
        )
        # send e-mail
        email.send()
        logger.info(
            f"Order confirmation email sent for order {order.id} to {order.email}"  # noqa
        )

    except Exception as e:
        logger.error(
            f"Failed to send confirmation email for order {order_id}: {e}"
        )
