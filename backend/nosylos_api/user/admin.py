from django.contrib import admin
from user.model_data.models.user import User
from user.model_data.models.user_profile import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "is_active",
        "is_newsletter_subscribed",
    )
    inlines = [
        UserProfileInline,
    ]
    search_fields = ("email",)
