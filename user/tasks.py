from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_account_deleted_email(user_email):
    """
    Task to send an e-mail notification once a user has deleted their account.
    """
    subject = "Your account has been deleted"
    message = (
        "Hello,\n\n"
        "This is to confirm that your account has been permanently deleted.\n"
        "We are sorry to see you go!\n\n"
        "If this was a mistake, feel free to create a new account at any time.\n\n"  # noqa
        "Best regards,\n"
        "The WebDev4U Team"
    )
    mail_sent = send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email]
        )
    return mail_sent
