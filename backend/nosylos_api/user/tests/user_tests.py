from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from rest_framework import status
from user.model_data.models.user import User
from utils.base_test_case import APITestCase


class UserTestCase(APITestCase):
    def test_register(self):
        # Data is not valid, request fails
        faulty_user_data = {
            "email": "test_userexample.com",
            "password": "test_password",
            "first_name": "",
            "last_name": "",
        }

        response = self.client.post(
            "/users/register/", format="json", data=faulty_user_data
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            b'{"email":["Enter a valid email address."]}', response.content
        )
        self.assertEqual(0, len(mail.outbox))

        # Request should succeed, input data is valid
        user_data = {
            "email": "test_user@example.com",
            "password": "test_password",
            "first_name": "",
            "last_name": "",
        }

        response = self.client.post(
            "/users/register/", format="json", data=user_data
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        user = User.objects.filter(email=user_data["email"]).first()
        self.assertIsNotNone(user)
        self.assertEqual("test", user.first_name)

        # Email confirmation email
        self.assertEqual(1, len(mail.outbox))
        self.assertIn(user.email, mail.outbox[0].body)
        self.assertIn(user.id, mail.outbox[0].body)
        self.assertEqual([user.email], mail.outbox[0].to)

        # First name data field take precedence over custom extraction logic
        user_data = {
            "email": "test_user1@example.com",
            "password": "test_password",
            "first_name": "Name",
            "last_name": "",
        }

        response = self.client.post(
            "/users/register/", format="json", data=user_data
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        user = User.objects.filter(email=user_data["email"]).first()
        self.assertIsNotNone(user)
        self.assertEqual(user_data["first_name"], user.first_name)
        # "is_newsletter_subscribed" not provided, defaults to True
        self.assertTrue(user.is_newsletter_subscribed)

        user_data2 = {
            "email": "test_user2@example.com",
            "password": "test_password2",
            "first_name": "Name2",
            "last_name": "",
            "is_newsletter_subscribed": False,
        }

        response = self.client.post(
            "/users/register/", format="json", data=user_data2
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        user2 = User.objects.filter(email=user_data2["email"]).first()
        self.assertIsNotNone(user2)
        self.assertEqual(user_data2["first_name"], user2.first_name)
        # "is_newsletter_subscribed" not provided, defaults to True
        self.assertFalse(user2.is_newsletter_subscribed)

    def test_user_update(self):
        self._login_user(self.staff_user)
        self.assertTrue(self.staff_user.is_newsletter_subscribed)
        response = self.client.patch(
            f"/users/{self.staff_user.id}/",
            format="json",
            data={"is_newsletter_subscribed": False},
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertFalse(
            User.objects.get(
                email=self.staff_user.email
            ).is_newsletter_subscribed
        )

    def test_confirm_email(self):
        # Request needs all parameters
        response = self.client.post(
            "/users/register/confirm_email/",
            data={
                "uid": self.staff_user.id,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual("Missing parameters", response.data["error"])

        # Request needs valid token
        response = self.client.post(
            "/users/register/confirm_email/",
            data={
                "uid": self.staff_user.id,
                "token": "invalid_token",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual("Input invalid", response.data["error"])

        self.assertFalse(self.staff_user.is_email_confirmed)

        token = default_token_generator.make_token(self.staff_user)
        response = self.client.post(
            "/users/register/confirm_email/",
            data={
                "uid": self.staff_user.id,
                "token": token,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(email=self.staff_user.email)
        self.assertTrue(user.is_email_confirmed)

    def test_send_confirmation_email(self):
        # Request needs all parameters
        response = self.client.post(
            "/users/register/send_confirmation_email/",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual("Missing email", response.data["error"])

        # User doesn't have email confirmed
        # email should be sent
        self.assertFalse(self.staff_user.is_email_confirmed)
        response = self.client.post(
            "/users/register/send_confirmation_email/",
            data={"email": self.staff_user.email},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(mail.outbox))
        self.assertIn(self.staff_user.email, mail.outbox[0].body)
        self.assertIn(self.staff_user.id, mail.outbox[0].body)
        self.assertEqual([self.staff_user.email], mail.outbox[0].to)

        # User already has email confirmed
        # email should not be sent
        self.staff_user.is_email_confirmed = True
        self.staff_user.save()
        response = self.client.post(
            "/users/register/send_confirmation_email/",
            data={"email": self.staff_user.email},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(mail.outbox))
