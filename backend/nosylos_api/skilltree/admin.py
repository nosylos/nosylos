from django.contrib import admin
from skilltree.model_data.models.badge import Badge
from skilltree.model_data.models.skill import Skill
from skilltree.model_data.models.skill_node import SkillNode
from skilltree.model_data.models.skill_point import SkillPoint


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "skill_node__name",
    )
    search_fields = ("name", "skill_node__name")


class SkillPointInline(admin.StackedInline):
    model = SkillPoint
    extra = 0


@admin.register(SkillPoint)
class SkillPointAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "skill_node__name",
    )
    search_fields = ("name", "skill_node__name")


class SkillNodeInline(admin.StackedInline):
    model = SkillNode
    extra = 0


@admin.register(SkillNode)
class SkillNodeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "skill",
        "skill__name",
    )
    inlines = [
        SkillPointInline,
    ]
    search_fields = ("name", "skill__id", "skill__name")


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
