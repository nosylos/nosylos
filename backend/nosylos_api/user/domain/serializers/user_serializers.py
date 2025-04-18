from rest_framework import serializers
from user.model_data.models.user import User


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=8, max_length=128, write_only=True
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "is_newsletter_subscribed",
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True, max_length=128)
    password = serializers.CharField(
        min_length=8, max_length=128, write_only=True
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "is_newsletter_subscribed",
            "is_email_confirmed",
        )

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
