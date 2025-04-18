from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string


# These util functions are wrappers around send_mail
# to handle the from/recipient
def send_mail_to_support(subject, message):
    sent_count = send_mail(
        subject=subject,
        message=message,
        from_email="noreply@nosylos.com",
        recipient_list=[settings.SUPPORT_EMAIL],
    )

    return sent_count != 0


def send_account_confirmation_email(user):
    if not user:
        return False

    token = default_token_generator.make_token(user)
    context = {
        "email": user.email,
        "confirm_url": (
            f"{settings.FRONTEND_URL}" f"/auth/confirm-email/{user.id}/{token}"
        ),
    }
    html_msg = render_to_string(
        template_name="./email_templates/confirm_email.html",
        context=context,
    )
    plain_message = render_to_string(
        template_name="./email_templates/confirm_email.txt",
        context=context,
    )

    sent_count = send_mail(
        subject="nosylos Confirmare email",
        message=plain_message,
        from_email="noreply@nosylos.com",
        recipient_list=[user.email],
        html_message=html_msg,
    )

    return sent_count != 0
