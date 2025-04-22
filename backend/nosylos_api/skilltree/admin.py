from django.contrib import admin
from skilltree.model_data.models.skill import Skill
from skilltree.model_data.models.skill_node import SkillNode


class SkillNodeInline(admin.StackedInline):
    model = SkillNode


@admin.register(SkillNode)
class SkillNodeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "skill",
    )
    search_fields = ("name", "skill__id")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "user",
    )
    inlines = [
        SkillNodeInline,
    ]
    search_fields = ("name", "user__id")
