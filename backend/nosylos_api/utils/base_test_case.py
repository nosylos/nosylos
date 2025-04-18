from rest_framework.test import APIClient
from rest_framework.test import APITestCase as BaseTestCase
from rest_framework_simplejwt.tokens import RefreshToken
from user.model_data.models.user import User


class APITestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.client = APIClient(hostname="localhost")
        self.staff_user = self._create_user(
            email="argus@nosylos.com",
            password="password",
            is_staff=True,
        )

    def _create_user(self, **kwargs):
        return User.objects.create(**kwargs)

    def _login_user(self, user):
        access_token = RefreshToken.for_user(user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
