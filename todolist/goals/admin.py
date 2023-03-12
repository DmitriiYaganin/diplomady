from django.contrib import admin

from todolist.goals.models import GoalCategory


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title',)


class GoalCommentsAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'created', 'updated')
    search_fields = ('text', 'description')


admin.site.register(GoalCategory, GoalCategoryAdmin)
