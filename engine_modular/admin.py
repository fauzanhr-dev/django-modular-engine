from django.contrib import admin

from .models import (
    Module
)


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("key", "title", "installed_version", "is_installed", "installed_at", "updated_at")
