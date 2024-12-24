from django.contrib import admin

from jars.models import Jar, JarOperation


@admin.register(Jar)
class JarAdmin(admin.ModelAdmin):
    list_display = ["title", "balance", "user", "goal"]
    prepopulated_fields = {"slug": ["title"]}


@admin.register(JarOperation)
class JarOperationAdmin(admin.ModelAdmin):
    list_display = ["jar", "amount", "created_at"]
