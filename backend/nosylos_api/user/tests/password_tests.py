from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from rest_framework import status
from user.model_data.models.user import User
from utils.base_test_case import APITestCase


class PasswordTestCase(APITestCase):
    def test_password_reset_email(self):
        # Email is required
        response = self.client.post(
            "/auth/password/reset_email/",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Email needs to belong to user
        # Request will return successful to not leak information
        # No email will be sent
        response = self.client.post(
            "/auth/password/reset_email/",
            data={"email": "fake_user@example.com"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(0, len(mail.outbox))

        response = self.client.post(
            "/auth/password/reset_email/",
            data={"email": self.staff_user.email},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual(
            "NoSylos Reset password request", mail.outbox[0].subject
        )
        self.assertIn(self.staff_user.email, mail.outbox[0].body)
        self.assertIn(self.staff_user.id, mail.outbox[0].body)
        self.assertEqual([self.staff_user.email], mail.outbox[0].to)

    def test_can_reset(self):
        # Request needs a token
        response = self.client.get(
            "/auth/password/can_reset/",
            data={
                "uid": self.staff_user.id,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(
            "/auth/password/can_reset/",
            data={"uid": self.staff_user.id, "token": "dsasjhdljklasnkajd"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.json()["canReset"])

        token = default_token_generator.make_token(self.staff_user)
        response = self.client.get(
            "/auth/password/can_reset/",
            data={"uid": self.staff_user.id, "token": token},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json()["canReset"])

    def test_reset(self):
        # Request needs all parameters
        response = self.client.post(
            "/auth/password/reset/",
            data={
                "uid": self.staff_user.id,
                "password1": "new_password",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Request needs valid token
        response = self.client.post(
            "/auth/password/reset/",
            data={
                "uid": self.staff_user.id,
                "token": "falsy_token",
                "password1": "new_password",
                "password2": "new_password",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        token = default_token_generator.make_token(self.staff_user)
        # Request needs matching passwords
        response = self.client.post(
            "/auth/password/reset/",
            data={
                "uid": self.staff_user.id,
                "token": token,
                "password1": "new_password",
                "password2": "new_passworddd",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["error"], "Password mismatch")

        response = self.client.post(
            "/auth/password/reset/",
            data={
                "uid": self.staff_user.id,
                "token": token,
                "password1": "new_password",
                "password2": "new_password",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(email=self.staff_user.email)
        self.assertTrue(user.check_password("new_password"))
        self.assertFalse(default_token_generator.check_token(user, token))
