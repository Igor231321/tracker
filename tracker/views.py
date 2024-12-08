from typing import Any
from django.views import generic

from tracker.models import Transaction, Category


class TransactionListView(generic.ListView):
    model = Transaction
    template_name = "tracker/index.html"
    context_object_name = "transations"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["categorys"] = Category.objects.all()
        return context


class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = "tracker/category.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["transactions"] = self.object.transactions.all()
        return context