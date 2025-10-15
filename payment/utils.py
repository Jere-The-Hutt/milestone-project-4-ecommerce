from io import BytesIO
import weasyprint
from django.contrib.staticfiles import finders
from django.template.loader import render_to_string


def generate_order_pdf(order):
    """
    Generate PDF invoice for an order and return BytesIO object.
    """
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(finders.find('css/pdf.css'))]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    out.seek(0)
    return out
