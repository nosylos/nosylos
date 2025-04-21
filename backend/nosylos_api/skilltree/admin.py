from django.contrib import admin
from skilltree.model_data.models.skill import Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "user",
    )
