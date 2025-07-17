import stripe
import logging
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order
from .tasks import payment_completed

logger = logging.getLogger(__name__)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    # --- Attempt to parse and verify the webhook ---
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        logger.error("Invalid payload: %s", e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error("Invalid signature: %s", e)
        return HttpResponse(status=400)

    # --- Log unhandled event types ---
    if event.type != 'checkout.session.completed':
        logger.warning("Unhandled event type: %s", event.type)
        return HttpResponse(status=200)  # Don't crash

    # --- Process the completed session ---
    session = event.data.object
    logger.info("Stripe Session: %s", session)

    if (
        session.get('mode') == 'payment' and
        session.get('payment_status') == 'paid'
    ):
        try:
            order = Order.objects.get(id=session.get('client_reference_id'))
        except Order.DoesNotExist:
            logger.error(
                "Order not found for ID: %s",
                session.get('client_reference_id')
                )
            return HttpResponse(status=404)

        order.paid = True
        order.stripe_id = session.get('payment_intent')
        order.save()
        # launch asynchronous task
        payment_completed.delay(order.id)
        logger.info("Order %s marked as paid", order.id)

    return HttpResponse(status=200)
