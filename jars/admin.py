from django.contrib import admin

from jars.models import Jar, JarOperation


@admin.register(Jar)
class JarAdmin(admin.ModelAdmin):
    list_display = ["title", "balance", "user", "goal"]
    prepopulated_fields = {"slug": ["title"]}
    search_fields = ["title", "balance", "user", "goal"]


@admin.register(JarOperation)
class JarOperationAdmin(admin.ModelAdmin):
    list_display = ["jar", "user", "amount", "created_at"]
    search_fields = ["jar", "user", "amount"]
