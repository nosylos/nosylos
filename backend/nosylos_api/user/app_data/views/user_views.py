from django.contrib.auth.tokens import default_token_generator
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from user.domain.queries.user_queries import get_user_no_exception
from user.domain.queries.user_queries import (
    handle_send_account_confirmation_email,
)
from user.domain.serializers.user_serializers import RegistrationSerializer
from user.domain.serializers.user_serializers import UserSerializer
from user.model_data.models.user import User


class RegistrationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        email = response.data.get("email")
        user = User.objects.filter(email=email).first()
        handle_send_account_confirmation_email(user, email)

        return response

    @action(detail=False, methods=["POST"])
    def confirm_email(self, request):
        if not (
            (uid := request.data.get("uid"))
            and (token := request.data.get("token"))
        ):
            return Response(
                {"error": "Missing parameters"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = get_user_no_exception(uid)
        if not (user and default_token_generator.check_token(user, token)):
            # Vague error message to avoid leaking DB information
            return Response(
                {"error": "Input invalid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.is_email_confirmed = True
        user.save()
        return Response()

    @action(detail=False, methods=["POST"])
    def send_confirmation_email(self, request):
        if not (email := request.data.get("email")):
            return Response(
                {"error": "Missing email"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(email=email).first()
        if user.is_email_confirmed:
            # Purposefully avoid notifying that the email is already confirmed
            # to not leak account information
            return Response()
        handle_send_account_confirmation_email(user, email)

        return Response()


class UserViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
