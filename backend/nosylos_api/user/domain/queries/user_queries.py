from django.core.exceptions import ValidationError
from django.core.mail import mail_admins
from user.model_data.models.user import User
from utils.mail_utils import send_account_confirmation_email


def get_user_no_exception(uid):
    try:
        user = User._default_manager.get(pk=uid)
    except (
        TypeError,
        ValueError,
        OverflowError,
        User.DoesNotExist,
        ValidationError,
    ):
        user = None
    return user


def handle_send_account_confirmation_email(user, email):
    if not user:
        mail_admins(
            subject="User creation or confirmation error",
            message=(
                f"User with email: {email} did not create/confirm successfully"
            ),
        )

    sent = send_account_confirmation_email(user)
    if not sent:
        mail_admins(
            subject="User confirmation email did not send",
            message=(
                "Could not send confirmation email to user with:\n"
                f"email: {email}\n"
                f"id: {user.id}\n"
            ),
        )
