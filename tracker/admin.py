from django.contrib import admin

from tracker.models import Category, Transaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display: list[str] = ["title"]
    prepopulated_fields = {"slug": ["title"]}


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["description", "amount", "created_at", "category", "status", "user"]
    list_filter = ["category", "status", "amount", "created_at"]
    search_fields = ["description", "amount", "created_at"]
    created_at_hierarchy = "created_at"
    list_editable = ["amount", "status", "category", "user"]
    list_per_page = 10
    raw_id_fields = ["user"]
