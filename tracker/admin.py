from django.contrib import admin

from tracker.models import Transaction, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display: list[str] = ["title"]
    prepopulated_fields = {"slug": ["title"]}


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["description", "amount", "date", "category", "transaction_type"]
    list_filter = ["amount", "date", "category", "transaction_type"]
    search_fields = ["description", "amount"]
    date_hierarchy = "date"
