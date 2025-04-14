from django.conf import settings
from django.contrib.auth import password_validation
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from user.domain.queries.user_queries import get_user_no_exception
from user.model_data.models.user import User


class PasswordViewSet(viewsets.GenericViewSet):
    queryset = None
    permission_classes = (AllowAny,)
    serializer_class = None

    @method_decorator(csrf_protect)
    @action(detail=False, methods=["POST"])
    def reset_email(self, request):
        if not (email := request.data.get("email")):
            return HttpResponseBadRequest("Email required")

        user = User.objects.filter(email=email).first()
        # Return a 200 status code here, but don't send email
        # Prevent malicious actors from figuring out if the email is in the DB
        if not user:
            return Response()

        token = default_token_generator.make_token(user)
        context = {
            "email": user.email,
            "reset_url": f"{settings.FRONTEND_URL}/auth/{user.id}/{token}",
        }
        html_msg = render_to_string(
            template_name="./email_templates/reset_password.html",
            context=context,
        )
        plain_message = render_to_string(
            template_name="./email_templates/reset_password.txt",
            context=context,
        )

        sent_count = send_mail(
            subject="NoSylos Reset password request",
            message=plain_message,
            from_email="noreply@nosylos.com",
            recipient_list=[user.email],
            html_message=html_msg,
        )

        if sent_count == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response()

    @action(detail=False, methods=["GET"])
    def can_reset(self, request):
        if not (
            (uid := request.query_params.get("uid"))
            and (token := request.query_params.get("token"))
        ):
            return HttpResponseBadRequest("Missing parameters")
        return Response({"can_reset": self._can_reset(uid, token)})

    @action(detail=False, methods=["POST"])
    def reset(self, request):
        if not (
            (uid := request.data.get("uid"))
            and (token := request.data.get("token"))
            and (password1 := request.data.get("password1"))
            and (password2 := request.data.get("password2"))
        ):
            return HttpResponseBadRequest("Missing parameters")

        if not self._can_reset(uid, token):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if password1 != password2:
            return Response(
                {"error": "Password mismatch"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = get_user_no_exception(uid)
        password_validation.validate_password(password2, user)
        user.set_password(password2)
        user.save()

        return Response(status=status.HTTP_200_OK)

    def _can_reset(self, uid, token):
        user = get_user_no_exception(uid)
        if user is None:
            return False
        if not default_token_generator.check_token(user, token):
            return False
        return True
