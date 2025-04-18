from django.contrib import admin
from user.model_data.models.user import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "is_active",
        "is_newsletter_subscribed",
    )


admin.site.register(User, UserAdmin)
